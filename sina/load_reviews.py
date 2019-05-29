from tools import get_html
from pyquery import PyQuery as pq
import time
import random
from urllib.parse import urlparse

channels = {"新浪娱乐": "yl", "音乐频道": "yl",

            "国内财经": "cj", "产经": "cj", "证券": "cj", "美股": "cj", "会议讲座": "cj", "港股": "cj", "国际财经": "cj", "外汇": "cj",
            "理财": "cj", "评论": "cj", "券商": "cj", "理财": "cj",

            "新浪科技": "kj", "国内新闻": "gn", "社会万象": "sh",
            "新浪体育": "ty", "新浪军事": "jc", "国际新闻": "gj"
            }


def __get_channel(html):
    doc = pq(html)
    channel_path = doc.find(".channel-path")
    all_text = channel_path.text().strip()
    if all_text != None and len(all_text) > 0:
        return all_text[:4]
        # if channel_path != None:
        #     nodes = channel_path.children()
        #     if len(nodes) > 0:
        #         text = nodes[0].text.strip()  # 获取第一个子标签
        #         print(text)


def __get_newsId(news_url):
    result = urlparse(news_url)
    print(result)


def urls_with_reviews(news_url):
    """获取存在评论的url"""
    return


def parse_news_page(news_url):
    '''解析新闻页,从里面获取新闻评论url'''
    html = get_html(news_url)
    channel = __get_channel(html)
    news_id = __get_newsId(news_url)
    comments_url = "http://comment5.news.sina.com.cn/comment/skin/default.html?channel=" + channel + "&newsid=" + news_id + "&group=0"
    return comments_url


def load_data(reviews_url):
    """ 获取评论 """
    pass


if __name__ == "__main__":
    from sina.index_url import main

    __get_newsId("http://finance.sina.com.cn/chanjing/gsnews/2019-05-29/doc-ihvhiews5306706.shtml")
