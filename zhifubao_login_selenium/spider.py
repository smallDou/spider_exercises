from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)


def login(name, pwd):
    url = "https://shenghuo.alipay.com/send/payment/fill.htm"
    browser.get(url)
    browser.implicitly_wait(3)
    try:
        li = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#J-loginMethod-tabs > li:nth-child(2)")))
        li.click()
        input_name = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#J-input-user")))
        input_name.clear()
        wait_input(input_name,name)
        time.sleep(1)
        input_pwd = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#password_rsainput")))
        input_pwd.clear()
        wait_input(input_pwd,pwd)
        time.sleep(1)
        #input_pwd.send_keys(Keys.RETURN)
        submit = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#J-login-btn")))
        time.sleep(1)
        submit.click()
    except TimeoutException:
        print("Time Out")
    finally:
        browser.quit()

def wait_input(input,str): #减缓输入速度
    for i in str:
        input.send_keys(i)
        time.sleep(0.5)

def main():
    login(NAME, PWD)


if __name__ == "__main__":
    main()