from abc import ABC, abstractmethod
from loguru import logger
from utils.http_utils import make_request

class BaseSpider(ABC):
    """
    爬虫基类，定义基本的爬虫接口
    """
    
    def __init__(self, name):
        self.name = name
        self.proxies = None
        logger.info(f"初始化爬虫: {name}")

    def set_proxy(self, proxy):
        """
        设置代理IP
        
        Args:
            proxy: 代理IP地址，例如 'http://127.0.0.1:1080'
        """
        if proxy:
            self.proxies = {"http": proxy, "https": proxy}
            logger.info(f"{self.name} 设置代理: {proxy}")
        else:
            self.proxies = None
            logger.info(f"{self.name} 未设置代理")

    def make_request(self, url, method='GET', headers=None, data=None, params=None):
        """
        发送HTTP请求
        
        Args:
            url: 请求URL
            method: 请求方法，'GET' 或 'POST'
            headers: 请求头
            data: 请求体数据
            params: URL参数
            
        Returns:
            响应对象
        """
        return make_request(url, method=method, headers=headers, data=data, params=params)

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
    
    @abstractmethod
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
