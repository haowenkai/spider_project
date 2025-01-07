from loguru import logger
from spiders.base_spider import BaseSpider

class ToutiaoHotSpider(BaseSpider):
    def __init__(self, use_proxy=False):
        super().__init__(use_proxy)
        self.base_url = "https://tophub.today/n/mproPpoq6O"  # 今日头条热榜
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_data(self):
        try:
            response = self.get(self.base_url, headers=self.headers)
            if response and response.status_code == 200:
                return response.text
            else:
                logger.error(f"请求失败，状态码: {response.status_code if response else 'N/A'}")
                return None
        except Exception as e:
            logger.error(f"请求出错: {e}")
            return None

    def parse(self, html):
        logger.info("开始解析今日头条热搜数据")
        hot_items = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='item')  # 假设每个热搜项都在一个 class 为 'item' 的 div 中
        for index, item in enumerate(items):
            rank_element = item.find('div', class_='index') # 假设排名在 class 为 'index' 的 div 中
            rank = rank_element.text.strip() if rank_element else str(index + 1)
            title_element = item.find('a')  # 假设标题在 a 标签中
            title = title_element.text.strip() if title_element else 'No Title'
            link_element = "https://tophub.today" + title_element['href'] if title_element and 'href' in title_element.attrs else None # 构建完整链接
            hot_value_element = item.find('div', class_='detail-hot')  # 假设热度值在 class 为 'detail-hot' 的 div 中
            hot_value = hot_value_element.text.strip() if hot_value_element else 'N/A'
            hot_items.append({
                'rank': rank,
                'title': title,
                'hot_value': hot_value,
                'url': link_element,
                'crawl_time': self.current_time
            })
        logger.info(f"找到 {len(hot_items)} 个热搜项")
        return hot_items

    def save_data(self, data):
        filename = f"toutiao_hot_{self.current_time}.json"
        self._save_json(data, filename)
        filename_csv = f"toutiao_hot_{self.current_time}.csv"
        self._save_csv(data, filename_csv)

    def run(self):
        logger.info("开始爬取今日头条热搜...")
        html_data = self.fetch_data()
        if html_data:
            parsed_data = self.parse_data(html_data)
            if parsed_data:
                self.save_data(parsed_data)
                logger.info(f"成功获取到 {len(parsed_data)} 条热搜数据")
                return parsed_data
            else:
                logger.error("解析今日头条热搜数据失败")
                return None
        else:
            logger.error("获取今日头条热搜HTML失败")
            return None

if __name__ == '__main__':
    spider = ToutiaoHotSpider()
    spider.run()
