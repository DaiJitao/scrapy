from tools import get_html
from pyquery import PyQuery as pq
import time
import random
from urllib.parse import urlparse
import pandas
from math import ceil, floor
from tools import times
import pandas as pd
import json


""" 获取新闻评论的数据接口url """

channels = {"新浪娱乐": "yl", "音乐频道": "yl",

            "国内财经": "cj", "产经": "cj", "证券": "cj", "美股": "cj", "会议讲座": "cj", "港股": "cj", "国际财经": "cj", "外汇": "cj",
            "理财": "cj", "评论": "cj", "券商": "cj", "理财": "cj",

            "新浪科技": "kj", "国内新闻": "gn", "社会万象": "sh",
            "新浪体育": "ty", "新浪军事": "jc", "国际新闻": "gj"
            }

cj = {'china', 'review', 'chanjing', 'meeting', 'roll', '7x24', 'world', 'money', 'stock'}


def __get_channel(html):
    """获取频道"""
    # doc = pq(html)
    # channel_path = doc.find(".channel-path")
    # all_text = channel_path.text().strip()
    # if all_text != None and len(all_text) > 0:
    #     return all_text[:4]
    # if channel_path != None:
    #     nodes = channel_path.children()
    #     if len(nodes) > 0:
    #         text = nodes[0].text.strip()  # 获取第一个子标签
    #         print(text)


# def formate_page_url(size, url):
#     pages = ceil(size / 10)
#     pass


# def __get_newsId(news_url):
#     result = urlparse(news_url)
#     print(result.path)


# def parse_news_page(news_url):
#     '''解析新闻页,从里面获取新闻评论url'''
#     # html = get_html(news_url)
#     channel = __get_channel(news_url)
#     news_id = __get_newsId(news_url)
#     comments_url = "http://comment5.news.sina.com.cn/comment/skin/default.html?channel=" + channel + "&newsid=" + news_id + "&group=0"
#     return comments_url

def get_data(page_num, url):
    data = []
    for i in range(1, page_num + 1):
        url_ = url.replace("page=1", "page=" + str(i))
        data_ = get_html(url_)  # 获取评论数据
        data.append(data_)
    return {"data": data}


def load_data(incsv, outpath=None):
    """ 获取评论 """
    url_info = pd.read_csv(incsv, header=None)
    result = []
    for i, (num, url) in url_info.iterrows():
        name = i + 1
        # print("读取%d..." % (name))
        page_num = ceil(num / 10)  # 获取页数
        data = get_data(page_num=page_num, url=url)
        breakTime = random.choice(times)
        time.sleep(breakTime)
        result = result + data["data"]
        if name % 500 == 0:  # 每隔500个url保存一次
            print("开始保存文件", len(result))
            outfile = outpath + str(name) + "_comments_data.csv"
            pd.DataFrame({"data": result}).to_csv(outfile, header=0, index=0)
            print("文件已经保存%s" % (outfile))
            result = []
    print("开始保存文件", len(result))
    outfile = outpath + str(name) + "_comments_data.csv"
    pd.DataFrame({"data": result}).to_csv(outfile, header=0, index=0)
    print("文件已经保存%s" % (outfile))


if __name__ == "__main__":
    out_path = "F:/scrapy/sina_data1.1.0/comments_data/resource/5/"
    incsv = "F:/scrapy/sina_data1.1.0/comments_data_url/all_data_5.csv"
    # load_data(incsv, out_path)

    cpu_cores = 8
    url_info = pd.read_csv(incsv, header=None)
    size, cols = url_info.shape
    size = 88
    yushu = size % cpu_cores
    interval = size // cpu_cores
    if yushu == 0:
        for i in range(cpu_cores):
            start = i * interval
            end = start + interval
            print((start, end))
    else:
        for i in range(cpu_cores):
            start = i * interval
            end = start + interval
            print((start, end))