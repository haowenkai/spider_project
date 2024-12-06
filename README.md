# Web Scraping Project

这是一个模块化的网络爬虫项目，提供了灵活且可扩展的爬虫框架。目前支持微博热搜等数据的采集。

## 项目结构

```
spider_project/
├── config/          # 配置文件目录
├── data/           # 数据存储目录
├── drivers/        # 浏览器驱动目录
├── logs/           # 日志文件目录
├── spiders/        # 爬虫脚本目录
│   └── weibo_hot.py  # 微博热搜爬虫
├── utils/          # 工具函数目录
├── main.py         # 主程序入口
├── requirements.txt # 项目依赖
└── README.md       # 项目说明文档
```

## 功能特性

- 模块化设计，易于扩展
- 支持无头浏览器模式
- 内置日志记录功能
- 数据自动保存为结构化格式

## 环境要求

- Python 3.8+
- Google Chrome 浏览器
- ChromeDriver（与Chrome版本匹配）

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖包：
- requests==2.31.0：HTTP请求库
- beautifulsoup4==4.12.2：HTML解析库
- selenium==4.18.1：浏览器自动化工具
- pandas==2.1.3：数据处理库
- loguru==0.7.2：日志记录工具

## ChromeDriver 配置

1. 检查Chrome浏览器版本
2. 从 https://googlechromelabs.github.io/chrome-for-testing/ 下载对应版本的ChromeDriver
3. 将下载的 chromedriver.exe 放置到项目的 drivers/ 目录下

## 使用说明

1. 克隆项目并安装依赖：
```bash
git clone [项目地址]
cd spider_project
pip install -r requirements.txt
```

2. 配置ChromeDriver（见上述说明）

3. 运行爬虫：
```bash
python main.py
```

## 数据输出

- 采集的数据将保存在 data/ 目录下
- 日志文件将保存在 logs/ 目录下

## 注意事项

- 请确保遵守网站的robots协议和使用条款
- 建议设置适当的请求间隔，避免对目标网站造成压力
- 首次运行前请确保已正确配置ChromeDriver
