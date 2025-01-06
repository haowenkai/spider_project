import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Style
from loguru import logger
from spiders.weibo_hot import WeiboHotSpider
from datetime import datetime

class WeiboHotGUI:
    def __init__(self, master):
        self.master = master
        master.title("微博热搜爬虫")
        master.configure(bg="lightgray")

        style = Style()
        style.theme_use('clam')
        style.configure('TButton', background='lightblue', foreground='black')

        self.start_button = ttk.Button(master, text="开始爬取", command=self.start_crawl)
        self.start_button.pack(pady=10)

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

        # 配置logger输出到GUI
        logger.add(self.log_to_gui, format="{time} {level} {message}", level="INFO")

        self.crawled_data = None

    def start_crawl(self):
        logger.info("开始爬取...")
        self.start_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        spider = WeiboHotSpider()
        self.crawled_data = spider.run()
        if self.crawled_data:
            logger.info(f"爬取完成，共获取 {len(self.crawled_data)} 条数据。")
            self.display_data()
            self.save_button.config(state=tk.NORMAL)
        else:
            logger.info("爬取失败。")
        self.start_button.config(state=tk.NORMAL)

    def display_data(self):
        for item in self.crawled_data:
            self.tree.insert('', tk.END, values=(item['rank'], item['title'], item['hot_value'], item['url'], item['crawl_time']))

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
                spider = WeiboHotSpider()
                if filename.endswith(".csv"):
                    if spider.save_to_csv(self.crawled_data, filename):
                        messagebox.showinfo("保存成功", f"数据已保存到 {filename}")
                    else:
                        messagebox.showerror("保存失败", "保存CSV文件失败，请查看日志。")
                elif filename.endswith(".json"):
                    if spider.save_to_json(self.crawled_data, filename):
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
