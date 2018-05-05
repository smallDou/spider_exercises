import requests
import re
from requests.exceptions import RequestException
from pymongo import MongoClient
from multiprocessing import Pool

client = MongoClient('localhost', 27017)  #建立MongoDB数据库连接
db = client['test']  #连接库名为test的数据库
collection = db['test']  #连接test集合


def get_page(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf8'  #设置utf-8编码,否则中文乱码
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_page(html):
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?</a>' +
        r'.*?title="(.*?)".*?</a></p>.*?star">(.*?)</p>.*?releasetime">' +
        r'(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:  #返回一个generator
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def save_to_Mongo(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_page(url)
    for item in parse_page(html):
        collection.insert(item)


if __name__ == '__main__':
    pool = Pool()  #创建进程池
    pool.map(save_to_Mongo, [i * 10 for i in range(10)])
    pool.close()  #不再创建进程
    pool.join()  #等待所有子进程执行完毕

client.close()