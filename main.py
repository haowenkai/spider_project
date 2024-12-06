from loguru import logger
import os
from config.settings import LOG_PATH, LOG_LEVEL
from spiders.weibo_hot import WeiboHotSpider

def setup_logging():
    """配置日志"""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    logger.add(LOG_PATH, level=LOG_LEVEL, rotation="500 MB")

def main():
    """主程序入口"""
    setup_logging()
    logger.info("爬虫程序启动")
    
    # 创建并运行微博热搜爬虫
    spider = WeiboHotSpider()
    html = spider.fetch_data()
    data = spider.parse_data(html)
    if data:
        spider.save_data(data)
        logger.info("微博热搜数据爬取完成")
    else:
        logger.error("未获取到微博热搜数据")
    
if __name__ == "__main__":
    main()
