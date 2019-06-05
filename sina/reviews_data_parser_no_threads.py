import json
import pandas
import csv


def save_data_to_csv(outpath, file_name, content):
    """
    :param path: 保存路径
    :param file_name: 文件名字
    :param res_queue:
    :return:
    """
    with open(outpath + file_name, mode='a', newline='', encoding='utf-8') as csvfile:  # 追加模式
        csv_write = csv.writer(csvfile, dialect="excel")
        # csv_write.writerow(["name", "age"])
        for data in content:
            try:
                csv_write.writerow(data)
            except UnicodeEncodeError as e:
                print("编码错误：", e, data)


def all_data_handler(incsv):
    data_ = pandas.read_csv(incsv, header=None, )
    data = data_.dropna(axis=0)  # 删除表中含有nan的行
    result = []
    for json in data[0]:
        result = result + __reviews_parser(json)
    return result


def __reviews_parser(content):
    """
    解析文件，提取数据
    :param content:
    :return:
    """
    result = []
    try:
        json_data = json.loads(content)  # dict
    except TypeError as e:
        print("读取数据%s\n，except:%s" % (content, e))

    if 'result' in json_data and 'cmntlist' in json_data['result']:
        cmntlist = json_data['result']['cmntlist']
        news = json_data['result']['news']
    else:
        cmntlist = []
    if (len(cmntlist) != 0):
        newsid = news['newsid']
        news_time = news["time"]
        news_url = news["url"]
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
            # res_queue.put(result)
    else:
        pass
    return result


if __name__ == "__main__":
    outpath = "F:/scrapy/sina_data1.1.0/comments_data/parsed/"
    file_name = '18000_all_data.csv'
    incsv_path = "F:/scrapy/sina_data1.1.0/comments_data/resource/"
    count = 0
    for i in range(36, 38): # 处理完18000
        name = (i + 1) * 500
        file = incsv_path + str(name) + "_comments_data.csv"
        # result = all_data_handler(file)
        # count = len(result) + count
        # save_data_to_csv(outpath, file_name, result)
    file = incsv_path + "19207_comments_data.csv"
    result = all_data_handler(file)
    save_data_to_csv(outpath, file_name, result)

    # save_data_to_csv(outpath=outpath,file_name=file_name, res_queue=res_queue)
    print("处理%d行完毕,文件保存%s" %(count, outpath + file_name))
