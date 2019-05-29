import requests
import random
from requests.exceptions import RequestException
import time
import os
import csv


def __get_page(index_url):
    print("access url: ", index_url)
    headers = {'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    try:
        response = requests.get(index_url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'  # 解决中文乱码
            return response.text
        else:
            return None
    except RequestException as e:
        print(e)
        return None


def get_html(index_url, try_times=3):
    '''默认重试次数3.'''
    for i in range(try_times):
        html = __get_page(index_url=index_url)
        if html != None:
            return html
        breakTime = random.choice([0.8, 1.5, 0.5, 1, 2.3, 1.8, 1, 2, 1.5, 0.5, 3, 1, 0.5, 1])
        time.sleep(breakTime)

def save_data_txt(file_path, name, data):
    try:
        os.makedirs(file_path)
    except:
        pass
    with open(file_path + name, 'w') as file:
        file.write(data)


def to_csv(path, file_name, data):
    """
    :param path: 保存路径
    :param file_name: 文件名字
    :param res_queue:
    :return:
    """
    if data == None:
        print("无数据保存")
    else:
        with open(path + file_name, mode='a', newline='', encoding='utf-8') as csvfile:
            csv_write = csv.writer(csvfile, dialect="excel")
            # csv_write.writerow(["name", "age"])
            for news in data:
                csv_write.writerow(news)

if __name__ == "__main__":
    url = "https://news.sina.com.cn/c/2019-05-29/doc-ihvhiews5310818.shtml"
    __get_page(url)