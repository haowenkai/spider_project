# Web Scraping Project

这是一个模块化的网络爬虫项目，提供了灵活且可扩展的爬虫框架。目前支持微博热搜等数据的采集。

## 项目特点

- 模块化设计，易于扩展新的爬虫
- 支持无头浏览器模式，减少资源占用
- 完善的日志记录功能
- 数据自动保存为结构化格式
- 异常处理机制，运行更稳定
- 支持代理设置，避免IP限制

## 项目结构

```
spider_project/
├── config/          # 配置文件目录
│   ├── __init__.py
│   └── settings.py  # 项目配置文件
├── data/           # 数据存储目录
├── drivers/        # 浏览器驱动目录
│   └── chromedriver.exe  # Chrome浏览器驱动
├── logs/           # 日志文件目录
├── spiders/        # 爬虫脚本目录
│   ├── __init__.py
│   ├── base_spider.py    # 基础爬虫类
│   └── weibo_hot.py      # 微博热搜爬虫
├── utils/          # 工具函数目录
│   ├── __init__.py
│   ├── http_utils.py     # HTTP请求工具
│   └── parser_utils.py   # 解析工具
├── main.py         # 主程序入口
├── requirements.txt # 项目依赖
└── README.md       # 项目说明文档
```

## 环境要求

- Python 3.8+
- Google Chrome 浏览器
- ChromeDriver（与Chrome版本匹配）

## 安装步骤

1. 克隆项目：
```bash
git clone https://github.com/haowenkai/spider_project.git
cd spider_project
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置ChromeDriver：
   - 检查Chrome浏览器版本
   - 从 https://googlechromelabs.github.io/chrome-for-testing/ 下载对应版本的ChromeDriver
   - 将chromedriver.exe放置到项目的drivers目录下

## 使用说明

1. 运行微博热搜爬虫：
```bash
python main.py
```

2. 数据输出：
   - 采集的数据将保存在data目录下
   - 日志文件将保存在logs目录下
   - 数据格式为CSV，包含标题、热度等信息

## 配置说明

在`config/settings.py`中可以修改以下配置：
- 数据保存路径
- 日志级别
- 请求间隔时间
- 代理设置
- 浏览器配置

## 注意事项

- 请遵守目标网站的robots协议
- 建议设置适当的请求间隔
- 首次运行前请确保已正确配置ChromeDriver
- 如遇到反爬限制，可以尝试：
  1. 增加请求间隔
  2. 使用代理IP
  3. 修改请求头信息

## 开发计划

- [ ] 添加更多数据源支持
- [ ] 优化数据存储方式
- [ ] 添加Web界面
- [ ] 支持定时任务
- [ ] 添加数据分析功能

## 问题反馈

如果您在使用过程中遇到任何问题，欢迎提交Issue或Pull Request。
