import requests
import random
from requests.exceptions import RequestException
import time
import os
import csv
from urllib.parse import urlparse
from multiprocessing import cpu_count
cpu_cores = cpu_count()

times = [0.8, 0.5, 0.1, 0, 1, 0.3, 0.1, 0.2]

def group_thread(size):
    gs = []
    interval = (size // cpu_cores)
    plus = size % cpu_cores
    for i in range(0, cpu_cores):
        if i == (cpu_cores - 1) and plus != 0:
            gs.append([end, size])
        else:
            start = i * interval
            end = start + interval
            gs.append([start, end])
    return gs

def __get_page(index_url):
    # print("access url: ", index_url)
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
        breakTime = random.choice(times)
        time.sleep(breakTime)


def mkdir(path):
    try:
        os.makedirs(path)
    except:
        pass


def save_data_txt(file_path, name, data):
    with open(file_path + name, 'w') as file:
        file.write(data)


def to_csv(path, file_name, data):
    """
    :param path: 保存路径
    :param file_name: 文件名字
    :param data: [ ["name", "age"] ]
    :return:
    """
    if data == None:
        print("无数据保存")
    else:
        with open(path + file_name, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_write = csv.writer(csvfile, dialect="excel")
            # csv_write.writerow(["name", "age"])
            for news in data:
                csv_write.writerow(news)


def all_index(data, v):
    result = []
    count = 0
    for value in data:
        if value == v:
            result.append(count)
        count += 1
    return result


def load_data_from_txt(file):
    result = set()
    with open(file, mode="r") as text:
        for line in text.readlines():
            tmp = line.strip()
            path = urlparse(tmp).path
            indexes = all_index(path, "/")
            start, second = indexes[0], indexes[1]
            channel = path[start + 1: second]
            result.add(channel)
    print(result)


def formate_time(time):
    if time < 10:
        return "0" + str(time)
    return str(time)


if __name__ == "__main__":
    print(formate_time(1))
