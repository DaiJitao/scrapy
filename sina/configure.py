
__comments_host = 'http://comment.sina.com.cn/page/info?version=1&format=json&'
callback = 'jsonp_1559217385884&_=1559217385884'
host_info = __comments_host

channels = {
    "ent_suda":"yl",
    "finance_0_suda":"cj",
    "news_china_suda":"gn",
    "news_mil_suda":"jc",
    "news_society_suda":"sh",
    "news_world_suda":"gj",
    "sports_suda":"ty",
    "tech_news_suda":"kj"
}

if __name__ == "__main__":
    print(channels["ent_suda"])