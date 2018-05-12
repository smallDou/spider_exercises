import requests
from settings import *
import random
import os

class Login(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self._data = {
            'username':self.username,
            'password':self.password,
            'savestate':'1',
            'r':'http://weibo.cn/',
            'ec':'0',
            'pagerefer':'',
            'entry':'mweibo',
        }
        self._user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
            'Mobile/13B143 Safari/601.1]',
            'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/48.0.2564.23 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/48.0.2564.23 Mobile Safari/537.36']
        self._headers = {
            'User_Agent': random.choice(self._user_agents),
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
        #save_to_redis()  考虑设置一个set存储cookie
                
if __name__ == '__main__':
    l = Login(USERNAME,PASSWORD)
    l.save_cookies()
    
