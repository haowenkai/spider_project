from loguru import logger
import os
from config.settings import LOG_PATH, LOG_LEVEL

def setup_logging():
    """配置日志"""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    logger.add(LOG_PATH, level=LOG_LEVEL, rotation="500 MB")

def main():
    """主程序入口"""
    setup_logging()
    logger.info("爬虫程序启动")

if __name__ == "__main__":
    main()
