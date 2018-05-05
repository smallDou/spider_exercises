from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlencode
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
import pickle
from bs4 import BeautifulSoup
import re
import requests
from pymongo import MongoClient
MONGO_URL = 'localhost'  #数据库设置
MONGO_DB = 'wechat'
MONGO_TABLE = '美食'

KEYWORD = '美食'

base_url = 'http://weixin.sogou.com/weixin?'

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)

client = MongoClient(MONGO_URL, 27017)  #建立MongoDB数据库连接
db = client[MONGO_DB]  #连接库名为Taobao的数据库
collection = db[MONGO_TABLE]  #连接product集合

#browser.add_cookie('cookie=')


def get_index_url(keyword):
    data = {'query': keyword, 'type': 2, 'page': 1}
    queries = urlencode(data)
    url = base_url + queries
    return url


def get_index_page(url):
    browser.get(url)
    get_details()


def next_page(page_number):
    try:
        submit = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#sogou_next')))
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#pagebar_container > span'),
                str(page_number)))
        get_details()
    except TimeoutException:
        print('Get_Next_page Error')


def get_details():
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#main > div.news-box > ul')))
        html = browser.page_source
        #print(html)
        soup = BeautifulSoup(html, 'lxml')
        items = soup.select('.news-box .news-list li .txt-box h3')
        for item in items:
            url = re.search(re.compile('href="(http://.*?)"'),
                            str(item)).group(1)
            url = re.sub('&amp', '', url)
            url = re.sub(';', '&', url)
            save_to_mongo(parse_details(url))
        # doc = pq(html)
        # items = doc('.txt-box h3 a').items()
        # for item in items:
        #     yield item.text()
    except TimeoutException:
        return get_details()


def parse_details(url):
    response = requests.get(url)
    html = response.text
    try:
        doc = pq(html)
        title = doc('#activity-name').text()
        date = doc('#post-date').text()
        nickname = doc('#post-user').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except Exception:
        return None


def save_to_mongo(product):
    try:
        if collection.insert(product):
            print('SAVE_TO_MONGO SUCCESS')
    except Exception:
        print('SAVE_TO_MONGO ERROR')

    else:
        return False


def main():
    url = get_index_url(KEYWORD)
    get_index_page(url)
    for i in range(2, 11):
        next_page(i)


if __name__ == '__main__':
    main()