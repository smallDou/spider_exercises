# -*- coding: utf-8 -*-
import requests
from os import path
import json
from login import Login
import re
import random
import time
from setting import query
import io
from db import MysqlClient

class Spider(object):
    def __init__(self,cookie,query=query):
        self.query = query
        self._header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }
        self._cookie = cookie
        self._token = ''
        self._article_num = 0

    @classmethod
    def verify_cookie(cls):
        with io.open(path.join(path.abspath('.'),'cookie.txt'),'r+') as f:
            cookie = f.read().encode('utf-8')
        if cookie:
            cookies = json.loads(cookie)
            return cls(cookie=cookies)
        else:
            l = Login()
            l.login()
            return cls(cookie=Spider.verify_cookie())

    def get_token(self):        
        url = 'https://mp.weixin.qq.com'
        response = requests.get(url,headers=self._header,cookies=self._cookie)
        self._token = re.findall(r'token=(\d+)',str(response.url))[0]
    
    def get_fakeid(self):
        self.get_token()
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        query_id = {
            'action': 'search_biz',
            'token' : self._token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5'
        }
        search_response = requests.get(search_url, cookies=self._cookie, headers=self._header, params=query_id)
        lists = search_response.json().get('list')[0]
        self._fakeid = lists.get('fakeid')

    def get_article_num(self):
        self.get_fakeid()
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        query_id_data = {
            'token': self._token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '0',#不同页，此参数变化，变化规则为每页加5
            'count': '5',
            'query': '',
            'fakeid': self._fakeid,
            'type': '9'
        }
        appmsg_response = requests.get(appmsg_url, cookies=self._cookie, headers=self._header, params=query_id_data)
        self._article_num = appmsg_response.json().get('app_msg_cnt')

    def save_to_mysql(self,query,title,url):
        m = MysqlClient()
        m.add(query,title,url)

    def get_details(self):
        self.get_article_num()
        num = int(int(self._article_num) / 5)
        begin = 0
        while num+1 > 0:
            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            query_id_data = {
                'token': self._token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),#不同页，此参数变化，变化规则为每页加5
                'count': '5',
                'query': '',
                'fakeid': self._fakeid,
                'type': '9'
            }
            query_fakeid_response = requests.get(appmsg_url, cookies=self._cookie, headers=self._header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')        
            for item in fakeid_list:
                #query是str  content_link是unicode
                content_link=item.get('link')
                content_title=item.get('title')
                # fileName=query+'.txt'
                # with io.open(path.join(path.abspath('.'),fileName),'a') as fh:
                #     fh.write(content_title+":\n"+content_link+"\n")
                self.save_to_mysql(query.decode('utf-8'),content_title,content_link)
            num -= 1
            begin = int(begin)
            begin+=5
            time.sleep(2)
  
if __name__ == '__main__':
    s = Spider.verify_cookie()
    s.get_details()
