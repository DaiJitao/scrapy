import json
import pandas
import csv
from multiprocessing import Queue
import threading

"""此线程版本还未成熟"""

def save_data_to_csv(outpath, file_name, res_queue):
    """
    :param path: 保存路径
    :param file_name: 文件名字
    :param res_queue:
    :return:
    """
    thread_name = threading.current_thread().getName()
    print(thread_name + "启动")
    with open(outpath + file_name, mode='a', newline='', encoding='utf-8') as csvfile:
        csv_write = csv.writer(csvfile, dialect="excel")
        # csv_write.writerow(["name", "age"])
        while not res_queue.empty():
            content = res_queue.get()
            for data in content:
                try:
                    csv_write.writerow(data)
                except UnicodeEncodeError as e:
                    print("编码错误：", e, data)


def all_data_handler(incsv, res_queue):
    thread_name = threading.current_thread().getName()
    print(thread_name)
    data = pandas.read_csv(incsv, header=None, )
    for json in data[0]:
        __reviews_parser(json, res_queue)


def __reviews_parser(content, res_queue):
    """
    解析文件，提取数据
    :param content:
    :return:
    """
    json_data = json.loads(content)  # dict
    if 'result' in json_data and 'cmntlist' in json_data['result']:
        cmntlist = json_data['result']['cmntlist']
        news = json_data['result']['news']
    else:
        cmntlist = []
    if (len(cmntlist) > 0):
        newsid = news['newsid']
        news_time = news["time"]
        news_url = news["url"]
        result = []
        for element in cmntlist:
            uid = element['uid']
            rank = element['rank']
            area = element["area"]
            content_ = element['content']
            nick = element["nick"]
            parent_nick = element["parent_nick"]
            parent_uid = element['parent_uid']
            time = element['time']
            # newsid = element['newsid']
            hot = element['hot']
            data = [uid, rank, area, content_, nick, parent_nick, parent_uid, time, newsid, hot, news_time, news_url]
            result.append(data)
        res_queue.put(result)


if __name__ == "__main__":
    outpath = "F:/scrapy/sina_data1.1.0/comments_data/parsed/"
    file_name = 'all_data.csv'

    res_queue = Queue()  # 队列
    incsv500 = "F:/scrapy/sina_data1.1.0/comments_data/resource/500_comments_data.csv"
    incsv1000 = "F:/scrapy/sina_data1.1.0/comments_data/resource/1000_comments_data.csv"

    cpu_cores = 8
    thread1 = threading.Thread(target=all_data_handler, args=(incsv500, res_queue), name="500file")
    thread2 = threading.Thread(target=all_data_handler, args=(incsv1000, res_queue), name="1000file")
    thread3 = threading.Thread(target=save_data_to_csv, args=(outpath, file_name, res_queue), name="savedata")
    thread1.start()
    thread2.start()


    thread1.join()
    thread2.join()

    thread3.start()
    thread3.join()

    # save_data_to_csv(outpath=outpath,file_name=file_name, res_queue=res_queue)
    print("数据处理完毕,文件保存", outpath + file_name)
