import requests
from bs4 import BeautifulSoup
from loguru import logger
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import zipfile
import io

class WeiboHotSpider:
    def __init__(self):
        self.url = "https://s.weibo.com/top/summary"
        self.driver = None
        self.setup_driver()
        
    def download_chromedriver(self):
        """从淘宝镜像下载对应版本的 ChromeDriver"""
        try:
            # 获取 Chrome 版本
            chrome_version = "130.0.6723"  # 根据你的 Chrome 版本修改
            
            # 构建下载URL
            download_url = f"https://registry.npmmirror.com/-/binary/chromedriver/{chrome_version}/chromedriver_win32.zip"
            
            # 下载文件
            logger.info(f"正在从淘宝镜像下载 ChromeDriver {chrome_version}")
            response = requests.get(download_url)
            
            if response.status_code == 200:
                # 创建 drivers 目录
                driver_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'drivers')
                os.makedirs(driver_dir, exist_ok=True)
                
                # 解压文件
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                    zip_ref.extractall(driver_dir)
                
                logger.info("ChromeDriver 下载并解压成功")
                return os.path.join(driver_dir, 'chromedriver.exe')
            else:
                raise Exception(f"下载失败，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"下载 ChromeDriver 失败: {e}")
            raise

    def setup_driver(self):
        """设置 Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
            
            driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'drivers', 'chromedriver.exe')
            if not os.path.exists(driver_path):
                raise FileNotFoundError(f"ChromeDriver不存在，请下载并放置到: {driver_path}")
            
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("成功初始化 Chrome WebDriver")
        except Exception as e:
            logger.error(f"设置 WebDriver 失败: {e}")
            raise
        
    def fetch_data(self):
        """获取微博热搜数据"""
        try:
            logger.info(f"正在请求URL: {self.url}")
            
            # 访问页面
            self.driver.get(self.url)
            
            # 等待页面加载
            time.sleep(random.uniform(2, 4))
            
            # 等待热搜列表出现
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list_a")))
            
            # 获取页面源码
            html = self.driver.page_source
            logger.debug(f"成功获取页面源码，长度: {len(html)}")
            
            return html
            
        except Exception as e:
            logger.error(f"获取微博热搜失败: {e}")
            return None
        
    def parse_data(self, html):
        """解析微博热搜数据"""
        if not html:
            logger.error("没有HTML内容可供解析")
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        hot_list = []
        
        try:
            items = soup.select('.list_a li')
            
            logger.debug(f"找到 {len(items)} 个热搜项")
            
            if not items:
                logger.error("未找到任何热搜数据，HTML结构可能已改变")
                logger.debug(f"页面内容片段: {html[:500]}")
                return []
                
            for item in items:
                try:
                    rank = item.select_one('.ranktop')
                    title = item.select_one('.hot_word')
                    hot_value = item.select_one('.star_num')
                    
                    if rank and title:
                        hot_list.append({
                            'rank': rank.text.strip(),
                            'title': title.text.strip(),
                            'hot_value': hot_value.text.strip() if hot_value else ''
                        })
                        logger.debug(f"成功解析热搜项: {rank.text.strip()}. {title.text.strip()}")
                except Exception as e:
                    logger.error(f"解析单个热搜项时出错: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"解析微博热搜数据失败: {e}")
            
        return hot_list
    
    def save_to_csv(self, data, filename=None):
        """保存数据到CSV文件"""
        if not data:
            logger.error("没有数据可供保存")
            return False
            
        try:
            if filename is None:
                filename = f"weibo_hot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logger.info(f"数据已保存到文件: {filename}")
            return True
        except Exception as e:
            logger.error(f"保存数据到CSV失败: {e}")
            return False
            
    def __del__(self):
        """清理资源"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("已关闭 WebDriver")
            except Exception as e:
                logger.error(f"关闭 WebDriver 时出错: {e}")
                
    def run(self):
        """运行爬虫"""
        logger.info("开始爬取微博热搜...")
        html = self.fetch_data()
        data = self.parse_data(html)
        if data:
            logger.info(f"成功获取到 {len(data)} 条热搜数据")
            self.save_to_csv(data)
            return data
        return None
