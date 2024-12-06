import requests
from bs4 import BeautifulSoup
from loguru import logger
import pandas as pd
from datetime import datetime
import os
import time
import random
import json
from pathlib import Path

class WeiboHotSpider:
    def __init__(self, use_proxy=False):
        self.url = "https://weibo.com/ajax/statuses/hot_band"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://weibo.com/hot/search',
        }
        self.use_proxy = use_proxy
        self.proxies = self._get_proxy() if use_proxy else None
        
    def _get_proxy(self):
        """获取代理IP"""
        try:
            # 这里可以替换为您的代理获取方式
            proxy = "http://127.0.0.1:7890"  # 示例代理地址
            return {
                'http': proxy,
                'https': proxy
            }
        except Exception as e:
            logger.error(f"获取代理失败: {e}")
            return None
        
    def fetch_data(self):
        """获取微博热搜数据"""
        try:
            logger.info(f"正在请求URL: {self.url}")
            
            # 添加随机延迟
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(
                self.url,
                headers=self.headers,
                proxies=self.proxies if self.use_proxy else None,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"成功获取数据，状态码: {response.status_code}")
                return data
            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"获取微博热搜失败: {e}")
            return None
        
    def parse_data(self, json_data):
        """解析微博热搜数据"""
        if not json_data or 'data' not in json_data:
            logger.error("没有数据可供解析")
            return []
        
        hot_list = []
        try:
            band_list = json_data['data']['band_list']
            
            logger.debug(f"找到 {len(band_list)} 个热搜项")
            
            for item in band_list:
                try:
                    hot_list.append({
                        'rank': item.get('rank', ''),
                        'title': item.get('note', ''),
                        'hot_value': item.get('raw_hot', ''),
                        'category': item.get('category', ''),
                        'topic_flag': item.get('topic_flag', 0),
                        'subject_label': item.get('subject_label', ''),
                        'word_scheme': item.get('word_scheme', ''),
                        'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                        'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
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
            # 创建data目录（如果不存在）
            data_dir = Path(__file__).parent.parent / 'data'
            data_dir.mkdir(exist_ok=True)
            
            if filename is None:
                filename = data_dir / f"weibo_hot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logger.info(f"数据已保存到文件: {filename}")
            
            # 同时保存为JSON格式
            json_file = str(filename).replace('.csv', '.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已保存到JSON文件: {json_file}")
            
            return True
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            return False
                
    def run(self):
        """运行爬虫"""
        logger.info("开始爬取微博热搜...")
        json_data = self.fetch_data()
        data = self.parse_data(json_data)
        if data:
            logger.info(f"成功获取到 {len(data)} 条热搜数据")
            self.save_to_csv(data)
            return data
        return None
