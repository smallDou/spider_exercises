from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from settings import USERNAME,PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys
from db import RedisClient
import json
from os import path

class Login(object):
    def __init__(self,username=USERNAME,password=PASSWORD):
        self._browser = webdriver.Chrome()
        self._wait = WebDriverWait(self._browser,10)

        self._browser.set_window_size(1400,900)

        self.username = username
        self.password = password
        
        self._cookie = {}

    def login(self):
        url = 'https://mp.weixin.qq.com/'
        self._browser.get(url)
        self._browser.implicitly_wait(3)
        try:
            input_username = self._wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#header > div.banner > div > div > form > div.login_input_panel > div:nth-child(1) > div > span > input")))
            input_username[0].clear()
            input_username[0].send_keys(self.username)

            input_password = self._wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#header > div.banner > div > div > form > div.login_input_panel > div:nth-child(2) > div > span > input")))
            input_password[0].clear()
            input_password[0].send_keys(self.password)
            ##记住我
            remember_me = self._wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#header > div.banner > div > div > form > div.login_help_panel > label > i")))
            remember_me[0].click()

            submit = self._wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#header > div.banner > div > div > form > div.login_btn_panel > a")))
            submit[0].click()
            time.sleep(10)
            ##存储cookies到本地
            self._browser.get(url)
            for cookie_item in self._browser.get_cookies():
                self._cookie[cookie_item['name']] = cookie_item['value']
            cookie_str = json.dumps(self._cookie)
            with open(path.join(path.abspath('.'),'cookie.txt'), 'w+', encoding='utf-8') as f:
                f.write(cookie_str)
        except TimeoutException:
            print("Time Out")
    
    '''存储到redis
    def save_to_redis(self):
        self.login()
        conn = RedisClient()
        conn.add(self._cookie)
    '''

if __name__ == '__main__':
    l = Login()
    l.login()