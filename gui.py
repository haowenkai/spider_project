import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Style
from loguru import logger
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import runpy
from spiders.weibo_hot import WeiboHotSpider
from spiders.douyin_hot import DouyinHotSpider
from spiders.toutiao_hot import ToutiaoHotSpider
from spiders.kuaishou_hot import KuaishouHotSpider
from datetime import datetime

class WeiboHotGUI:
    def __init__(self, master):
        self.master = master
        master.title("微博热搜爬虫")
        master.configure(bg="lightgray")

        style = Style()
        style.theme_use('clam')
        style.configure('TButton', background='lightblue', foreground='black')

        # 创建一个 Frame 来放置按钮
        button_frame = ttk.Frame(master)
        button_frame.pack(pady=10)

        self.weibo_button = ttk.Button(button_frame, text="爬取微博", command=self.start_weibo_crawl)
        self.weibo_button.pack(side=tk.LEFT, padx=5)

        self.douyin_button = ttk.Button(button_frame, text="爬取抖音", command=self.start_douyin_crawl)
        self.douyin_button.pack(side=tk.LEFT, padx=5)

        self.toutiao_button = ttk.Button(button_frame, text="爬取今日头条", command=self.start_toutiao_crawl)
        self.toutiao_button.pack(side=tk.LEFT, padx=5)

        self.kuaishou_button = ttk.Button(button_frame, text="爬取快手", command=self.start_kuaishou_crawl)
        self.kuaishou_button.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(master, columns=('rank', 'title', 'hot_value', 'url', 'crawl_time'), show='headings')
        self.tree.heading('rank', text='排名')
        self.tree.heading('title', text='标题')
        self.tree.heading('hot_value', text='热度值')
        self.tree.heading('url', text='链接')
        self.tree.heading('crawl_time', text='爬取时间')
        self.tree.pack(pady=10)

        self.save_button = ttk.Button(master, text="保存数据", command=self.save_data, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.log_text = tk.Text(master, height=5, width=80)
        self.log_text.pack(pady=10)

        # 用于显示词云图的 Canvas
        self.wordcloud_canvas = tk.Canvas(master, width=800, height=400)
        self.wordcloud_canvas.pack(pady=10)

        # 配置logger输出到GUI
        logger.add(self.log_to_gui, format="{time} {level} {message}", level="INFO")

        self.crawled_data = None

    def start_weibo_crawl(self):
        logger.info("开始爬取微博热搜...")
        self.weibo_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        self.spider = WeiboHotSpider()
        self.crawled_data = self.spider.run()
        if self.crawled_data:
            logger.info(f"微博热搜爬取完成，共获取 {len(self.crawled_data)} 条数据。")
            self.display_data()
            self.generate_and_display_wordcloud()
            self.save_button.config(state=tk.NORMAL)
        else:
            logger.info("微博热搜爬取失败。")
        self.weibo_button.config(state=tk.NORMAL)
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Style
from loguru import logger
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import runpy
from spiders.weibo_hot import WeiboHotSpider
from spiders.douyin_hot import DouyinHotSpider
from spiders.toutiao_hot import ToutiaoHotSpider
from spiders.kuaishou_hot import KuaishouHotSpider
from datetime import datetime

class WeiboHotGUI:
    def __init__(self, master):
        self.master = master
        master.title("微博热搜爬虫")
        master.configure(bg="lightgray")

        style = Style()
        style.theme_use('clam')
        style.configure('TButton', background='lightblue', foreground='black')

        # 创建一个 Frame 来放置按钮
        button_frame = ttk.Frame(master)
        button_frame.pack(pady=10)

        self.weibo_button = ttk.Button(button_frame, text="爬取微博", command=self.start_weibo_crawl)
        self.weibo_button.pack(side=tk.LEFT, padx=5)

        self.douyin_button = ttk.Button(button_frame, text="爬取抖音", command=self.start_douyin_crawl)
        self.douyin_button.pack(side=tk.LEFT, padx=5)

        self.toutiao_button = ttk.Button(button_frame, text="爬取今日头条", command=self.start_toutiao_crawl)
        self.toutiao_button.pack(side=tk.LEFT, padx=5)

        self.kuaishou_button = ttk.Button(button_frame, text="爬取快手", command=self.start_kuaishou_crawl)
        self.kuaishou_button.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(master, columns=('rank', 'title', 'hot_value', 'url', 'crawl_time'), show='headings')
        self.tree.heading('rank', text='排名')
        self.tree.heading('title', text='标题')
        self.tree.heading('hot_value', text='热度值')
        self.tree.heading('url', text='链接')
        self.tree.heading('crawl_time', text='爬取时间')
        self.tree.pack(pady=10)

        self.save_button = ttk.Button(master, text="保存数据", command=self.save_data, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.log_text = tk.Text(master, height=5, width=80)
        self.log_text.pack(pady=10)

        # 用于显示词云图的 Canvas
        self.wordcloud_canvas = tk.Canvas(master, width=800, height=400)
        self.wordcloud_canvas.pack(pady=10)

        # 配置logger输出到GUI
        logger.add(self.log_to_gui, format="{time} {level} {message}", level="INFO")

        self.crawled_data = None

    def start_weibo_crawl(self):
        logger.info("开始爬取微博热搜...")
        self.weibo_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        self.spider = WeiboHotSpider()
        self.crawled_data = self.spider.run()
        if self.crawled_data:
            logger.info(f"微博热搜爬取完成，共获取 {len(self.crawled_data)} 条数据。")
            self.display_data()
            self.generate_and_display_wordcloud()
            self.save_button.config(state=tk.NORMAL)
        else:
            logger.info("微博热搜爬取失败。")
        self.weibo_button.config(state=tk.NORMAL)

    def start_douyin_crawl(self):
        logger.info("开始爬取抖音热搜...")
        self.douyin_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        self.spider = DouyinHotSpider()
        self.crawled_data = self.spider.run()
        if self.crawled_data:
            logger.info(f"抖音热搜爬取完成，共获取 {len(self.crawled_data)} 条数据。")
            self.display_data()
            logger.info(f"准备生成词云，抖音数据是否为空: {not self.crawled_data}")
            self.generate_and_display_wordcloud()
            self.save_button.config(state=tk.NORMAL)
        else:
            logger.info("抖音热搜爬取失败。")
        self.douyin_button.config(state=tk.NORMAL)

    def start_toutiao_crawl(self):
        logger.info("开始爬取今日头条热搜...")
        self.toutiao_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        self.spider = ToutiaoHotSpider()
        self.crawled_data = self.spider.run()
        if self.crawled_data:
            logger.info(f"今日头条热搜爬取完成，共获取 {len(self.crawled_data)} 条数据。")
            self.display_data()
            logger.info(f"准备生成词云，今日头条数据是否为空: {not self.crawled_data}")
            self.generate_and_display_wordcloud()
            self.save_button.config(state=tk.NORMAL)
        else:
            logger.info("今日头条热搜爬取失败。")
        self.toutiao_button.config(state=tk.NORMAL)

    def start_kuaishou_crawl(self):
        logger.info("开始爬取快手热搜...")
        self.kuaishou_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        self.spider = KuaishouHotSpider()
        self.crawled_data = self.spider.run()
        if self.crawled_data:
            logger.info(f"快手热搜爬取完成，共获取 {len(self.crawled_data)} 条数据。")
            self.display_data()
            logger.info(f"准备生成词云，快手数据是否为空: {not self.crawled_data}")
            self.generate_and_display_wordcloud()
            self.save_button.config(state=tk.NORMAL)
        else:
            logger.info("快手热搜爬取失败。")
        self.kuaishou_button.config(state=tk.NORMAL)

    def display_data(self):
        for item in self.crawled_data:
            self.tree.insert('', tk.END, values=(item['rank'], item['title'], item['hot_value'], item['url'], item['crawl_time']))

    def generate_and_display_wordcloud(self):
        import pandas as pd
        from analysis.analysis import generate_wordcloud
        if self.crawled_data:
            df = pd.DataFrame(self.crawled_data)
            logger.info(f"generate_and_display_wordcloud 函数接收到的数据前 5 行: {df.head()}")
            wordcloud_figure = generate_wordcloud(df)
            logger.info("成功生成词云 Figure 对象。")
            # 清空之前的画布内容
            self.wordcloud_canvas.delete("all")
            canvas_agg = FigureCanvasTkAgg(wordcloud_figure, master=self.wordcloud_canvas)
            canvas_agg.draw()
            canvas_agg_widget = canvas_agg.get_tk_widget()
            canvas_agg_widget.pack()
            logger.info("词云已添加到 Canvas。")
        else:
            logger.warning("没有数据可以生成词云。")

    def save_data(self):
        if self.crawled_data:
            filetypes = (
                ('CSV 文件', '*.csv'),
                ('JSON 文件', '*.json'),
                ('所有文件', '*.*')
            )
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=filetypes
            )
            if filename:
                if filename.endswith(".csv"):
                    if hasattr(self, 'spider') and hasattr(self.spider, 'save_to_csv') and self.spider.save_to_csv(self.crawled_data, filename):
                        messagebox.showinfo("保存成功", f"数据已保存到 {filename}")
                    else:
                        messagebox.showerror("保存失败", "保存CSV文件失败，请查看日志。")
                elif filename.endswith(".json"):
                    if hasattr(self, 'spider') and hasattr(self.spider, 'save_to_json') and self.spider.save_to_json(self.crawled_data, filename):
                        messagebox.showinfo("保存成功", f"数据已保存到 {filename}")
                    else:
                        messagebox.showerror("保存失败", "保存JSON文件失败，请查看日志。")
            else:
                messagebox.showinfo("提示", "取消保存。")
        else:
            messagebox.showinfo("提示", "没有数据可以保存。")

    def log_to_gui(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = WeiboHotGUI(root)
    root.mainloop()
