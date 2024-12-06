from abc import ABC, abstractmethod
from loguru import logger
from utils.http_utils import make_request

class BaseSpider(ABC):
    """
    爬虫基类，定义基本的爬虫接口
    """
    
    def __init__(self, name):
        self.name = name
        logger.info(f"初始化爬虫: {name}")
    
    @abstractmethod
    def parse(self, response):
        """
        解析响应数据的抽象方法
        
        Args:
            response: 响应对象
            
        Returns:
            解析后的数据
        """
        pass
    
    def start_requests(self):
        """
        开始请求的抽象方法
        """
        pass
    
    def save_data(self, data):
        """
        保存数据的方法
        
        Args:
            data: 要保存的数据
        """
        pass
