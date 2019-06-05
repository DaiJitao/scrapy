from urllib.parse import urlsplit, urlparse
from sina.configure import host_info, callback
from tools import get_html, formate_time
from pyquery import PyQuery as pq
import pandas
import json
from sina.configure import channels
from sina.SInaException import SinaException
import time
import random
from selenium import webdriver

times = [0.8, 1.5, 0.5, 1, 2.3, 1.8, 1, 2, 1.5, 0.5, 3, 1, 0.5, 1]

'''用户获取带有评论的url
'''


def comments_num(comments_url):
    """ js 渲染  从评论页面获取 """
    # html = get_html(comments_url)
    driver = webdriver.PhantomJS()  # 渲染
    driver.get(comments_url)
    html = driver.page_source
    driver.close()
    doc = pq(html)
    text = doc.find(".hd.clearfix").text()
    i = text.index('条')
    num = text[:i]
    return int(num)


def url_with_reviews_data(channel, id, page="1"):
    """获取评论数据 """
    url = "http://comment.sina.com.cn/page/info?version=1&format=json&" \
          "channel=" + channel + "&newsid=comos-" + id + "&group=undefined&compress=0&ie=utf-8&oe=utf-8&" \
                                                         "page=" + page + "&page_size=10&t_size=3&h_size=3&thread=1&uid=unlogin_user"
    return url


def urls_with_reviews(news_url, channel):
    '''
    获取存在评论的url 过滤url
    :param news_url:
    :param channel:
    :param page: 最小值1
    :return: [num, data_url]
    '''
    path = urlsplit(news_url).path[::-1]
    start_index = path.index(".") + 1
    second = path.index("-")
    id = path[start_index:second][::-1]
    id = id[1:]  # 去掉i 新闻id
    middle = "channel=" + channel + "&newsid=comos-" + id
    comments_url = "http://comment5.news.sina.com.cn/comment/skin/default.html?" + middle + "&group=0"  # 新闻评论网页
    data_url = url_with_reviews_data(channel=channel, id=id)  # 获取新闻评论数据的接口
    data = get_html(data_url)
    data = json.loads(data)
    try:
        num = data["result"]["count"]["show"]  # 获取评论的数量
    except Exception as e:
        raise SinaException(data_url)
    if int(num) > 0:
        return [num, data_url]
    return None


def get_news_url_from_csv(incsv_file, except_url):
    '''读取csvw文件， 获取新闻url
    :param incsv_file:
    :param except_url:
    :return:
    '''
    data = pandas.read_csv(incsv_file, header=None)
    result = []
    for _, (url, channel) in data.iterrows():
        channel_ = channels[channel]  # 所在新闻了类型
        try:
            num_data_url = urls_with_reviews(url, channel_)  # [num, data_url]
        except SinaException as e:
            tmp = {"访问的新闻网址出错": [url], "新闻评论数据接口": [e.errorObj]}
            pandas.DataFrame(tmp).to_csv(except_url, mode='a', header=0, index=0) # 异常新闻的保存
        if num_data_url != None:
            result.append(num_data_url)
    return result  # [[num, data_url]]


def main():
    except_url = r"F:\scrapy\sina_data1.1.0\except_url\url.csv"
    outfile = r"F:\scrapy\sina_data1.1.0\comments_data_url\all_data_5.csv"
    nums = []
    data_urls = []
    for i in range(1, 31):
        breakTime = random.choice(times)
        if i > 20:
            time.sleep(breakTime)
        i = formate_time(i)
        incsv = "F:/scrapy/sina_data1.1.0/news_detail_url/201905" + i + "/all_parsed.csv"
        data = get_news_url_from_csv(incsv_file=incsv, except_url=except_url)
        for t in data:
            nums.append(t[0])
            data_urls.append(t[1])

    all = {"nums": nums, 'data_urls': data_urls}
    pandas.DataFrame(all).to_csv(outfile, header=0, index=0)
    print("----> ok!")


if __name__ == "__main__":
    url = "https://news.sina.com.cn/c/gat/2019-04-01/doc-ihsxncvh7219805.shtml"
    (num, url) = urls_with_reviews(url, 'gn')
    print(num, url)

    data = pandas.read_csv(r"F:\scrapy\sina_data1.1.0\news_detail_url\20190401\all_parsed.csv", header=None)
    print(data.shape)
    d1 = list(data[0])
    d2 = list(data[1])
    #
    # data = pandas.DataFrame({"channel": d1, "url": d2})
    # data.to_csv("E:/dddd.csv", index=0, header=0)
    # main()
