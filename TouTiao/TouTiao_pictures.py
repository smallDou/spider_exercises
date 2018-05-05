import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import json
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
from multiprocessing import Pool
client = MongoClient('localhost', 27017)  #建立MongoDB数据库连接
db = client['TouTiao']  #连接库名为TouTiao的数据库
collection = db['TouTiao']  #连接TouTiao集合


def get_index_page(offset, keyword):  #关键词
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    params = urlencode(data)
    base = 'https://www.toutiao.com/search_content/'
    url = base + '?' + params
    response = requests.get(url)
    response.encoding = 'utf8'
    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ConnectionError:
        print('Connect Error')
        return None


def parse_index_page(response):
    try:
        data = json.loads(response)  #解析json对象
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        print('josn_loads Error')


def get_detail_page(url):
    if url:
        url = url.replace('group/', 'a')  #替换为跳转后的url
        response = requests.get(url)
        try:
            if response.status_code == 200:
                return response.text
            else:
                return None
        except ConnectionError:
            print('Connect Error')
            return None
    else:
        print('Get_detail_url Error')


def parse_detail_page(html, url):  #这个url为未跳转前的url
    if html:
        soup = BeautifulSoup(html, 'lxml')
        result = soup.select('title')  #选择含有title标签的
        title = result[0].get_text() if result else ''
        # images_pattern = re.compile(
        #     r'.*?img\ssrc.*?(http:\/\/.*?)\&quot;\simg_width',
        #     re.S)  #用正则表达式找到隐藏的url
        # images = re.findall(images_pattern, html)
        # return {'title': title, 'url': url, 'images': images}
        images_pattern = re.compile(r'gallery: JSON.parse\("(.*)"\)',
                                    re.S)  #json.parse 将str转化成json
        result = re.search(images_pattern, html)
        if result:
            data = json.loads(result.group(1).replace('\\', ''))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                # for image in images:
                #     download_image(image)
                return {'title': title, 'url': url, 'images': images}
    else:
        print('Get_detail_page Error')


def save_to_momgo(result):
    if collection.insert(result):
        print('Successfully Saved to Mongo')
        return True
    else:
        return False


def main(offset):
    keyword = '街拍'
    response = get_index_page(offset, keyword)
    urls = parse_index_page(response)
    for url in urls:
        html = get_detail_page(url)
        result = parse_detail_page(html, url)
        if result: save_to_momgo(result)


if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(0, 21)])
    pool.map(main, groups)
    pool.close()
    pool.join()