from bs4 import BeautifulSoup
from loguru import logger

def parse_html(html_content, parser='lxml'):
    """
    解析HTML内容
    
    Args:
        html_content (str): HTML内容
        parser (str): 解析器类型，默认为'lxml'
        
    Returns:
        BeautifulSoup: BeautifulSoup对象
    """
    try:
        return BeautifulSoup(html_content, parser)
    except Exception as e:
        logger.error(f"解析HTML失败: {str(e)}")
        raise

def extract_text(element, strip=True):
    """
    提取元素中的文本内容
    
    Args:
        element: BeautifulSoup元素
        strip (bool): 是否去除首尾空白字符
        
    Returns:
        str: 提取的文本内容
    """
    if element is None:
        return ""
    text = element.get_text()
    return text.strip() if strip else text
