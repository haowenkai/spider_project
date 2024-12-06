import requests
from loguru import logger
from config.settings import DEFAULT_HEADERS, REQUEST_TIMEOUT

def make_request(url, method='GET', headers=None, params=None, data=None):
    """
    发送HTTP请求的通用方法
    
    Args:
        url (str): 请求URL
        method (str): 请求方法，默认为'GET'
        headers (dict): 请求头
        params (dict): URL参数
        data (dict): 请求体数据
        
    Returns:
        requests.Response: 响应对象
    """
    try:
        _headers = DEFAULT_HEADERS.copy()
        if headers:
            _headers.update(headers)
            
        response = requests.request(
            method=method,
            url=url,
            headers=_headers,
            params=params,
            data=data,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"请求失败: {url}, 错误: {str(e)}")
        raise
