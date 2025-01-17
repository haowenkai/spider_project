import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import jieba
from wordcloud import WordCloud
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def generate_wordcloud(df):
    """
    生成词云图并返回 Figure 对象。
    """
    titles = ' '.join(df['title'].tolist())
    wc = WordCloud(width=800, height=400, background_color="white", font_path="C:\\Windows\\Fonts\\msyh.ttc")
    wc.generate(titles)
    fig = plt.Figure(figsize=(10, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    ax.set_title("热搜词云")
    return fig

def analyze_hot_data(data_path):
    """
    分析热点数据，包括词频统计和热度分析。
    """
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"找不到文件: {data_path}")
        return

    # 1. 词频统计
    titles = ' '.join(df['title'].tolist())
    words = jieba.cut(titles)
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(10)
    print("\n词频统计 (Top 10):")
    for word, count in most_common_words:
        print(f"{word}: {count}")

    # 3. 热度分析 (假设数据包含 'hot_value' 列)
    if 'hot_value' in df.columns:
        df['crawl_time'] = pd.to_datetime(df['crawl_time'])
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['crawl_time'], df['hot_value'])
        ax.set_xlabel("时间")
        ax.set_ylabel("热度")
        ax.set_title("热度随时间变化")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        plt.show()
    else:
        print("\n数据中不包含 'hot_value' 列，无法进行热度分析。")

if __name__ == "__main__":
    # 示例用法，假设最新的数据文件名为 weibo_hot_latest.csv
    latest_data_file = "data/weibo_hot_latest.csv"  # 需要根据实际情况修改
    analyze_hot_data(latest_data_file)
