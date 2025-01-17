from loguru import logger
import os
from config.settings import LOG_PATH, LOG_LEVEL
from analysis.analysis import analyze_hot_data
import glob
import tkinter as tk
from gui import WeiboHotGUI

def setup_logging():
    """配置日志"""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    logger.add(LOG_PATH, level=LOG_LEVEL, rotation="500 MB")

def main():
    """主程序入口"""
    setup_logging()
    logger.info("爬虫程序启动")

    # 获取最新的数据文件
    # list_of_files = glob.glob('data/weibo_hot_*.csv')
    # if list_of_files:
    #     latest_file = max(list_of_files, key=os.path.getctime)
    #     analyze_hot_data(latest_file)
    # else:
    #     logger.warning("没有找到 Weibo 热搜数据文件，无法进行数据分析。")

    # 启动 GUI
    root = tk.Tk()
    gui = WeiboHotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
