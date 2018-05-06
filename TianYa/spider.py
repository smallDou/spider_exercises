import requests
from urllib.parse import urlencode
import re
from pyquery import PyQuery as pq 
from bs4 import BeautifulSoup
from lxml import etree

KEYWORD = '妹子'

baseurl = 'http://search.tianya.cn/bbs'

def get_page(url,keyword,pn):
    data = {
        'q': keyword,
        'pn': pn,
    }
    params = urlencode(data)
    page_url = url + '?' + params
    try:
        response = requests.get(page_url)
        if response.status_code == 200:
            return response.text
        else:
            get_page(url,keyword,pn)
    except ConnectionError:
        print('get_page error')
        get_page(url,keyword,pn)

def parse_page(response):
    ##顺便测试一下速度，发现beautiful比较慢，xpath次之，正则最快
    '''正则
    pattern = re.compile('<h3><a\shref="(.*?)"\starget',re.S)
    items = re.findall(pattern,response)
    for url in items:
        yield url
    '''
    '''beautiful
    soup = BeautifulSoup(response,'lxml')
    for url in soup.select('h3.a'):
        yield url
    '''
    '''xpath
    '''
    html = etree.HTML(response)
    urls = html.xpath('//h3/a/@href')
    for url in urls:
        yield url

def get_total_page(response):
    pattern = re.compile('<strong>(\d*)</strong>.*<a\shref=\'javascript:go\(\d*\);\'>(\d*)</a>',re.S)
    item = re.search(pattern,response)
    curr_page , total_page = item.group(1) , item.group(2)
    print(total_page)
    return total_page

def parse_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = etree.HTML(response.text)
            title = html.xpath('//span[@class="s_title"]/span/text()')
            items = html.xpath('//div[@class="bbs-content clearfix"]/text()')
            content = ''
            for item in items:
                content = content + item.strip()
            print(title,list(content))
            save_to_mongo()
    except ConnectionError:
        print('pase_details error')
        parse_details(url)

def save_to_mongo():
    pass

def main():
    response = get_page(baseurl,KEYWORD,1)
    total_page = get_total_page(response)
    for curr_page in range(1,int(total_page)+1):
        response = get_page(baseurl,KEYWORD,curr_page)
        for item in parse_page(response):
            print(item)
            parse_details(item)

if __name__ == '__main__':
    main()
    