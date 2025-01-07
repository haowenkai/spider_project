from loguru import logger
from spiders.base_spider import BaseSpider

class KuaishouHotSpider(BaseSpider):
    def __init__(self, use_proxy=False):
        super().__init__(use_proxy)
        self.base_url = "https://m.kuaishou.com/m_batch/long/list? EisnerId=new_front"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8'
        }

    def fetch_data(self):
        try:
            response = self.post(self.base_url, headers=self.headers, json={"page": 1})
            if response and response.status_code == 200:
                return response.json()
            else:
                logger.error(f"请求失败，状态码: {response.status_code if response else 'N/A'}")
                return None
        except Exception as e:
            logger.error(f"请求出错: {e}")
            return None

    def parse(self, json_data):
        logger.info("开始解析快手热搜数据")
        hot_items = []
        if json_data and 'feeds' in json_data:
            for index, item in enumerate(json_data['feeds']):
                rank = index + 1
                title = item.get('caption', 'No Title')
                link = f"https://m.kuaishou.com/short-video/{item.get('id')}" if item.get('id') else None
                hot_value = item.get('viewCount', 'N/A') # 假设使用 viewCount 作为热度值
                hot_items.append({
                    'rank': rank,
                    'title': title,
                    'hot_value': hot_value,
                    'url': link,
                    'crawl_time': self.current_time
                })
        logger.info(f"找到 {len(hot_items)} 个热搜项")
        return hot_items

    def save_data(self, data):
        filename = f"kuaishou_hot_{self.current_time}.json"
        self._save_json(data, filename)
        filename_csv = f"kuaishou_hot_{self.current_time}.csv"
        self._save_csv(data, filename_csv)

    def run(self):
        logger.info("开始爬取快手热搜...")
        json_data = self.fetch_data()
        if json_data:
            parsed_data = self.parse_data(json_data)
            if parsed_data:
                self.save_data(parsed_data)
                logger.info(f"成功获取到 {len(parsed_data)} 条热搜数据")
                return parsed_data
            else:
                logger.error("解析快手热搜数据失败")
                return None
        else:
            logger.error("获取快手热搜数据失败")
            return None

if __name__ == '__main__':
    spider = KuaishouHotSpider()
    spider.run()
