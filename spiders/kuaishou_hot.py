from loguru import logger
from .base_spider import BaseSpider
from datetime import datetime
import json
import pandas as pd

class KuaishouHotSpider(BaseSpider):
    def __init__(self):
        super().__init__(name="快手热搜")
        self.base_url = "https://m.gifshow.com/fw/hot?fid=692989317&cc=share_copylink&followRefer=1733395983&shareObjectId=749948787707113503&shareMethod=COPY_LINK&kpn=KUAISHOU&subBiz=FEEDS&sharePhotoId=749948787707113503&shareToken=X-ea0a9b0a739a4451a-I&appType=1&utm_source=app_share&relationType=3&memoryPipelineAB="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }
        self.current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    def start_requests(self):
        logger.info("开始爬取快手热搜...")
        response = super().make_request(self.base_url, headers=self.headers)
        if response and response.status_code == 200:
            self.parse(response)
        else:
            logger.error(f"请求失败，状态码: {response.status_code if response else 'N/A'}")

    def parse(self, response):
        logger.info("开始解析快手热搜数据")
        html = response.text
        hot_items = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find('script', string=lambda text: text and 'window.__INITIAL_STATE__' in text)
        if script_tag:
            json_content = script_tag.string.split('=')[1].strip()[:-1]
            data = json.loads(json_content)
            trends = data.get('hotPage', {}).get('trends', [])
            for item_data in trends:
                rank = item_data.get('index')
                title = item_data.get('title')
                url = f"https://m.gifshow.com/fw/trend/{item_data.get('id')}?fid=692989317&cc=share_copylink&followRefer=1733395983&shareObjectId=749948787707113503&shareMethod=COPY_LINK&kpn=KUAISHOU&subBiz=FEEDS&sharePhotoId=749948787707113503&shareToken=X-ea0a9b0a739a4451a-I&appType=1&utm_source=app_share&relationType=3&memoryPipelineAB="
                hot_value = item_data.get('heat')
                hot_items.append({
                    'rank': rank,
                    'title': title,
                    'hot_value': hot_value,
                    'url': url,
                    'crawl_time': self.current_time
                })
            logger.info(f"找到 {len(hot_items)} 个热搜项")
            self.save_data(hot_items)
            return hot_items
        else:
            logger.error("未找到包含热搜数据的 script 标签")
            return []

    def save_data(self, data):
        filename = f"data/kuaishou_hot_{self.current_time}.json"
        self._save_json(data, filename)
        filename_csv = f"data/kuaishou_hot_{self.current_time}.csv"
        self._save_csv(data, filename_csv)

    def _save_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"数据已保存到 JSON 文件: {filename}")

    def _save_csv(self, data, filename_csv):
        df = pd.DataFrame(data)
        df.to_csv(filename_csv, encoding='utf-8-sig', index=False)
        logger.info(f"数据已保存到 CSV 文件: {filename_csv}")

    def run(self):
        self.start_requests()

if __name__ == '__main__':
    spider = KuaishouHotSpider()
    spider.run()
