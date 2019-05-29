from tools import get_html, save_data_txt, to_csv
from sina.parser import parse_home_data

'''
获取所有新闻的url
'''


class ParserURL:
    def __init__(self, index_url, out_url=None):
        self.index_url = index_url
        self.out_url = out_url

    def all_news_url(self, out_home_page, out_home_page_name="all_news"):
        """ 获取新闻总排行url """
        home_html = get_html(self.index_url).strip()
        print("home_html", home_html)
        if out_home_page != None and out_home_page_name != None:
            save_data_txt(out_home_page, out_home_page_name, home_html)  # 保存数据
        news_data = parse_home_data(home_html)
        to_csv(out_home_page, "parsed_all_news.csv", news_data)
        result = []
        for news in news_data:
            result.append(news[2])
        return result

    def domestic_news(self, save_path, save_name="domestic_news.txt"):
        '''国内新闻'''
        home_html = get_html(self.index_url).strip()
        print("home_html", home_html)
        if save_path != None and save_name != None:
            save_data_txt(save_path, save_name, home_html)  # 保存数据
        news_data = parse_home_data(home_html)
        to_csv(save_path, "parsed_domestic_news.csv", news_data)  # 保存解析数据
        result = []
        for news in news_data:
            result.append(news[2])
        return result

    def international_news(self):
        '''国际新闻'''
        pass

    def social_news(self):
        '''社会新闻'''
        pass

    def sports_news(self):
        '''体育新闻'''
        pass

    def financial_news(self):
        '''财经新闻'''
        pass

    def entertainment_News(self):
        '''娱乐新闻'''
        pass

    def technology_News(self):
        '''科技新闻'''
        pass

    def military_News(self):
        '''军事新闻'''
        pass


def load_all_url(news_url):
    parser = ParserURL(news_url)
    p1 = parser.xinwen_zong_paihang_url()
    p2 = parser.domestic_news()
    return set(p1 + p2)


def main():
    home_page = "F:/scrapy/sina_data1.1.0/"
    home_page_name = "all_news_data.txt"
    # 国内新闻url
    url = 'http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_0_suda&top_time=20190529&top_show_num=100&top_order=DESC&js_var=channel_'
    parser = ParserURL(index_url=url)
    urls = parser.all_news_url(out_home_page=home_page, out_home_page_name=home_page_name)
    print(urls)
    print(len(urls))
    return urls
