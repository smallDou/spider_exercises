from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
MONGO_URL = 'localhost' #数据库设置
MONGO_DB = 'taobao'
MONGO_TABLE = 'fruit'

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']  #PhantomJs设置

KEYWORD = '水果'  #关键字

#browser = webdriver.Chrome()
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 10)  #设置浏览器等待时间

browser.set_window_size(1400, 900)  #设置窗口大小

client = MongoClient(MONGO_URL, 27017)  #建立MongoDB数据库连接
db = client[MONGO_DB]  #连接库名为Taobao的数据库
collection = db[MONGO_TABLE]  #连接product集合

def search():  #搜索关键字
    browser.get('https://www.taobao.com')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#J_TSearchForm > div.search-button > button")))
        input.send_keys(KEYWORD)  #输入关键字
        submit.click()  #设置点击
        total = wait.until(  #获取总页面数
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text  #!!!调用total.text()显示调用该方法错误
    except TimeoutException:
        return search()


def next_page(page_number):  #设置自动翻页
    try:
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 '#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'
            )))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((
                By.CSS_SELECTOR,
                '#mainsrp-pager > div > div > div > ul > li.item.active > span'
            ), str(page_number)))
        get_products()
    except TimeoutException:
        return next_page(page_number)


def get_products():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    #beautifulsoup解析网页
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('#mainsrp-itemlist .items .item')  #css选择器选择
    for item in items:
        product = {}
        for imgs in item.select('.pic img'):
            product['img'] = re.search(  #正则匹配src
                re.compile(r'data-src="(.*?)"\sid=', re.S), str(imgs)).group(1)
        for price in item.select('.price'):
            product['price'] = price.get_text().strip()
        for deal in item.select('.deal-cnt'):
            product['deal'] = deal.get_text().strip()[:-3]
        for title in item.select('.title'):
            product['title'] = title.get_text().strip()
        for shop in item.select('.shop'):
            product['shop'] = shop.get_text().strip()
        for location in item.select('.location'):
            product['location'] = location.get_text().strip()
        print(product)
        if product:
            save_to_mongo(product)
    # doc = pq(html)     #pyquery 解析html网页
    # items = doc('#mainsrp-itemlist .items .item').items()
    # for item in items:
    #     product = {
    #         'image': item.find('.pic .img').attr('src'),
    #         'price': item.find('.price').text(),
    #         'deal': item.find('.deal-cnt').text()[:-3],
    #         'title': item.find('.title').text(),
    #         'shop': item.find('.shop').text(),
    #         'location': item.find('.location').text()
    #     }
    #     print(product)
    #正则解析   !!!出错
    # pattern = re.compile(
    #     r'<div\sclass="pic">.*?<img\sid.*?data-src="(.*?)"\salt=' +
    #     r'.*?<div\sclass="price\sg_price\sg_price-highlight">.*?<strong>(.*?)</strong>.*?' +
    #     r'<div\sclass="deal-cnt">(.*?)</div>.*?<div\sclass="row\srow-2\stitle">.*?trace-pid=.*?>(.*?)<span\sclass="H"' +
    #     r'.*?<span\sclass="dsrs">.*?</span>\s<span>(.*?)</span>.*?<div\sclass="location">(.*?)</div>',
    #     re.S)
    # items = re.findall(pattern,doc)
    # print(items)
    # for item in items:
    #     yield  {
    #         'image': item[0],
    #         'price': item[1],
    #         'deal': item[2],
    #         'title': item[3].strip(),  #去除首尾空格
    #         'shop': item[4],
    #         'localtion': item[5]
    #     }


def save_to_mongo(product):
    try:
        if collection.insert(product):
            print('SAVE_TO_MONGO SUCCESS')
    except Exception:
        print('SAVE_TO_MONGO ERROR')
    
    else:
        return False


def main():
    try:
        total = search()
        total = int(re.compile(r'(\d+)').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print('GET_NEXT_PAGE ERROR')
    finally:
        browser.close()


if __name__ == '__main__':
    main()