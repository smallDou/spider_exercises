import requests
from settings import USERNAME,PASSWORD,User_Agent
import random
import os
from db import RedisClient

class Login(object):
    def __init__(self,username=USERNAME,password=PASSWORD,user_agent=User_Agent):
        self._data = {
            'username':username,
            'password':password,
            'savestate':'1',
            'r':'http://weibo.cn/',
            'ec':'0',
            'pagerefer':'',
            'entry':'mweibo',
        }
        self._headers = {
            'User_Agent': random.choice(user_agent),
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
            'Origin': 'https://passport.weibo.cn',
            'Host': 'passport.weibo.cn'
        }
        self._cookie = {}
        self._file = os.path.join(os.path.dirname(__file__),'cookies.txt')

    def login(self):
        #!!!!模拟登陆一定要保持session
        session = requests.session()
        login_url = 'https://passport.weibo.cn/sso/login'
        response = session.post(login_url,data=self._data,headers=self._headers)
        if response.status_code == 200:
            self._cookie = response.cookies.get_dict()            
        else:
            print('login error')
            return None
        
    def save_cookies(self):
        self.login()
        conn = RedisClient()
        conn.add(self._cookie)
        #print(self._cookie)
                
if __name__ == '__main__':
    l = Login()
    l.save_cookies()
    
