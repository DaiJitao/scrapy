import json
import csv




def parse_home_data(content):
    ''' 解析新闻排行数据 '''
    part1 = content[:27]
    if "{" in part1:
        index = part1.index('{')
        str_data = content[index:-1]
        print("str_data", str_data)
        json_data = json.loads(str_data)
        result = []
        if "data" in json_data:
            data_arr = json_data['data']
            for news in data_arr:
                id = news['id']
                title = news['title']
                media = news['media']
                author = news['author']
                comment_url = news['comment_url']
                url = news['url']
                create_date = news['create_date']
                create_time = news['create_time']
                cat_name = news['cat_name']
                top_time = news['top_time']
                top_num = news['top_num']
                time = news['time']
                tmp = [id, title, url, comment_url, create_date, create_time, media, author, cat_name, top_time,
                       top_num, time]
                result.append(tmp)
        return result
    else:
        print("home data: ", content)
        return []
