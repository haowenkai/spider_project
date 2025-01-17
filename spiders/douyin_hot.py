from datetime import datetime
from loguru import logger
from .base_spider import BaseSpider

class DouyinHotSpider(BaseSpider):
    def __init__(self):
        super().__init__(name="抖音热搜")
        self.base_url = "https://www.douyin.com/hot/billboard"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    def start_requests(self):
        logger.info("开始爬取抖音热搜...")
        response = super().make_request(self.base_url, headers=self.headers)
        if response and response.status_code == 200:
            self.parse(response)
        else:
            logger.error(f"请求失败，状态码: {response.status_code if response else 'N/A'}")

    def parse(self, response):
        logger.info("开始解析抖音热搜数据")
        html = response.text
        hot_items = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='aweme-item')
        for index, item in enumerate(items):
            rank = index + 1
            title_element = item.find('a', class_='title')
            title = title_element.text.strip() if title_element else 'No Title'
            link_element = "https://www.douyin.com" + title_element['href'] if title_element and 'href' in title_element.attrs else None
            hot_value_element = item.select_one('span.hot')
            hot_value = hot_value_element.text.strip() if hot_value_element else 'N/A'
            hot_items.append({
                'rank': rank,
                'title': title,
                'hot_value': hot_value,
                'url': link_element,
                'crawl_time': self.current_time
            })
        logger.info(f"找到 {len(hot_items)} 个热搜项")
        self.save_data(hot_items)
        return hot_items

    def save_data(self, data):
        filename = f"data/douyin_hot_{self.current_time}.json"
        self._save_json(data, filename)
        filename_csv = f"data/douyin_hot_{self.current_time}.csv"
        self._save_csv(data, filename_csv)

    def _save_json(self, data, filename):
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"数据已保存到 JSON 文件: {filename}")

    def _save_csv(self, data, filename_csv):
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv(filename_csv, encoding='utf-8-sig', index=False)
        logger.info(f"数据已保存到 CSV 文件: {filename_csv}")

    def run(self):
        self.start_requests()

if __name__ == '__main__':
    spider = DouyinHotSpider()
    spider.run()
