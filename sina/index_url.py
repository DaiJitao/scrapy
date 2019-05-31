from tools import get_html, save_data_txt, to_csv, mkdir
from sina.parser import parse_home_data, get_channel
import pandas as pd

'''
获取所有新闻的url
'''


class NewsHomeURL:
    '''获取新闻主页入口地址'''

    def news_3url(self, top_cat, top_time, top_show_num='100'):
        '''
        top_cat=news_china_suda top_time=20190529&top_show_num=20
        :param top_cat:  新闻类型
        :param top_time: 发布时间
        :param top_show_num: 显示条数
        :return:
        '''
        channels = ['news_china_suda', 'news_world_suda', 'news_society_suda']
        if top_cat in channels:
            url = "http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=" + top_cat \
                  + "&top_time=" + top_time + "&top_show_num=" + str(top_show_num) + "&top_order=DESC&js_var=news_"
            return url
        else:
            print("新闻频道错误：", top_cat, "不在", channels, '里面')
            return None

    def integrated_channel(self, time, num='100'):
        url = 'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=www_www_all_suda_suda&' \
              'top_time=' + time + '&top_show_num=' + num + '&top_order=DESC&js_var=all_1_data01'
        return url

    def sports_url(self, time, num='100'):
        '''体育新闻'''
        url = 'http://top.sports.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=sports_suda&' \
              'top_time=' + time + '&top_show_num=' + num + '&top_order=DESC&js_var=channel_'
        return url

    def finance_url(self, time, num='100'):
        '''财经新闻'''
        url = 'http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_0_suda&' \
              'top_time=' + time + '&top_show_num=' + num + '&top_order=DESC&js_var=channel_'
        return url

    def entertainment_url(self, time, num='100'):
        '''娱乐新闻'''
        url = 'http://top.ent.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=ent_suda&' \
              'top_time=' + time + '&top_show_num=' + num + '&top_order=DESC&js_var=channel_'
        return url

    def technology_url(self, time, num='100'):
        '''科技新闻'''
        url = 'http://top.tech.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=tech_news_suda&' \
              'top_time=' + time + '&top_show_num=' + num + '&top_order=DESC&js_var=channel_'
        return url

    def military_url(self, time, num='100'):
        '''军事新闻 time='20190529 '''
        url = 'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_mil_suda&' \
              'top_time=' + time + '&top_show_num=' + num + '&top_order=DESC&js_var=channel_'
        return url


def get_news_detail_url(index_url, out_path=None):
    '''
    :param out_home_page:
    :param out_home_page_name:
    :return:
    '''
    channel = get_channel(url=index_url)  # 获取新闻频道
    home_html = get_html(index_url).strip()  # 访问的新闻类型url
    news_data = parse_home_data(home_html)  # 解析新闻数据
    if out_path != None:
        mkdir(out_path)
        save_data_txt(out_path, channel + "_resource.txt", home_html)  # 保存数据
        to_csv(out_path, channel + "_parsed.csv", news_data)
    result = dict()
    for news in news_data:
        news_id = news[0]
        url = news[2]
        # tmp = {"news_id":news_id, "url":url, "channel":channel}
        result[str(news_id)] = (url, channel)

    return result


def load_url(time):
    reslut = dict()
    num = '100'
    purl = NewsHomeURL()
    channels = ['news_china_suda', 'news_world_suda', 'news_society_suda']
    out_path = "F:/scrapy/sina_data1.1.0/news_detail_url/" + time + "/"
    for c in channels:
        url = purl.news_3url(c, time,
                             top_show_num=100)  # finance_url(time)# entertainment_url(time)# military_url(time) # technology_url(time) #sports_url(time)
        news_detail_url = get_news_detail_url(url, out_path)
        reslut.update(news_detail_url)

    in_url = purl.integrated_channel(time, num)
    sports = purl.sports_url(time, num)
    cj = purl.finance_url(time, num)
    yl = purl.entertainment_url(time, num)
    kj = purl.technology_url(time, num)
    jc = purl.military_url(time, num)

    in_url = get_news_detail_url(in_url, out_path)
    sports = get_news_detail_url(sports, out_path)
    cj = get_news_detail_url(cj, out_path)
    yl = get_news_detail_url(yl, out_path)
    kj = get_news_detail_url(kj, out_path)
    jc = get_news_detail_url(jc, out_path)

    # reslut.update(in_url)
    reslut.update(sports)
    reslut.update(cj)
    reslut.update(yl)
    reslut.update(kj)
    reslut.update(jc)
    path = "F:/scrapy/sina_data1.1.0/news_detail_url/" + time + "/"
    name = "all_parsed.csv"
    # 数据保存 pd.Series(reslut).to_csv(file, index=False) pd.Series(in_url).to_csv(int_file, index=False)
    tmp = []
    for url, channel in reslut.values():
        tmp.append([url, channel])
    to_csv(path, name, tmp)
    tmp = []
    for url, channel in in_url.values():
        tmp.append([url, channel])
    to_csv(path, "integrated_parsed.csv", tmp) # 新闻综合保存
    return reslut


def main():
    month = '04'
    for i in range(1, 31):
        if i < 10:
            date = '2019' + month + '0' + str(i)
            load_url(date)
        else:
            date = '2019' + month + str(i)
            load_url(date)

if __name__ == "__main__":
    main()