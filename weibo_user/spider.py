import requests
from db import RedisClient,MongoDB
from settings import User_Agent
import random
from login import Login
from lxml import etree
import re
from datetime import datetime,timedelta

class Spider(object):
    def __init__(self,cookie,user_id=1669879400,user_agent=User_Agent,filter=0):
        self._headers={
            'User_Agent': random.choice(user_agent),
        }
        self._cookie = cookie
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.username = ''  # 用户名，如“Dear-迪丽热巴”
        self.weibo_content = ''  # 微博内容
        self.publish_time = ''  # 微博发布时间
        self.up_num = ''  # 微博对应的点赞数
        self.retweet_num = ''  # 微博对应的转发数
        self.comment_num = ''  # 微博对应的评论数

    ##用@classmethod实现调用前验证cookie
    @classmethod 
    def verify_cookie(cls):
        baseurl = 'https://weibo.cn/'
        conn = RedisClient()
        if conn.get():
            #print(conn.get())
            try:
                response = requests.get(baseurl,cookies=conn.get())
                #print(response.text)                
                if response.status_code == 200:
                    return cls(cookie=conn.get())
                else:
                    conn.add_score(conn.get())
                    return cls(cookie=Spider.verify_cookie())
            except Exception:
                print('verify error')
        else:
            l = Login()
            l.save_cookies()
            return cls(cookie=Spider.verify_cookie())

    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            #print(url)
            response = requests.get(url, cookies=self._cookie,headers=self._headers)
            html = etree.HTML(response.text.encode('utf-8'))
            username = html.xpath('/html/body/div[7]/text()[1]')
            self.username = username[0].split(':')[1]
            #print(self.username)
        except Exception:
            print('get_username error')
        
        # 获取"长微博"全部文字内容
    def get_long_weibo(self, weibo_link):
        try:
            response = requests.get(weibo_link, cookies=self._cookie).text
            html = etree.HTML(response)
            info = html.xpath("//div[@class='c']")[1]
            wb_content = info.xpath("div/span[@class='ctt']")[0].xpath(
                "string(.)")
            #print(wb_content)
            return wb_content
        except Exception:
            print("get_long_weibo error")
            
    def save_to_mongo(self,dic):
            mon = MongoDB()
            if not mon.find({'内容':self.weibo_content}):
                mon.insert(dic)

    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):
        try:
            self.get_username()
            #print(self.username)
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            response = requests.get(url,cookies=self._cookie)
            html = etree.HTML(response.text.encode('utf-8'))
            if html.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(html.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                response2 = requests.get(url2, cookies=self._cookie)
                html2 = etree.HTML(response2.text.encode('utf-8'))
                info = html2.xpath("//div[@class='c']")
                is_empty = info[0].xpath("div/span[@class='ctt']")
                if is_empty:
                    for i in range(0, len(info) - 2):
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibo_content = str_t[0].xpath("string(.)")
                        weibo_content = weibo_content[:-1]
                        weibo_id = info[i].xpath("@id")[0][2:]
                        a_link = info[i].xpath(
                            "div/span[@class='ctt']/a/@href")
                        if a_link:
                            if a_link[-1] == "/comment/" + weibo_id:
                                weibo_link = "https://weibo.cn" + a_link[-1]
                                wb_content = self.get_long_weibo(weibo_link)
                                if wb_content:
                                    weibo_content = wb_content
                        self.weibo_content = weibo_content
                        #print(weibo_content)

                        # 微博发布时间
                        str_time = info[i].xpath("div/span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)")
                        publish_time = str_time.split(u'来自')[0]
                        if u"刚刚" in publish_time:
                            publish_time = datetime.now().strftime(
                                '%Y-%m-%d %H:%M')
                        elif u"分钟" in publish_time:
                            minute = publish_time[:publish_time.find(u"分钟")]
                            minute = timedelta(minutes=int(minute))
                            publish_time = (
                                datetime.now() - minute).strftime(
                                "%Y-%m-%d %H:%M")
                        elif u"今天" in publish_time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            time = publish_time[3:]
                            publish_time = today + " " + time
                        elif u"月" in publish_time:
                            year = datetime.now().strftime("%Y")
                            month = publish_time[0:2]
                            day = publish_time[3:5]
                            time = publish_time[7:12]
                            publish_time = (
                                year + "-" + month + "-" + day + " " + time)
                        else:
                            publish_time = publish_time[:16]
                        self.publish_time = publish_time
                        #print(publish_time)

                        str_footer = info[i].xpath("div")[-1]
                        str_footer = str_footer.xpath("string(.)")
                        str_footer = str_footer[str_footer.rfind(u'赞'):]
                        guid = re.findall(pattern, str_footer, re.M)

                        # 点赞数
                        up_num = int(guid[0])
                        self.up_num = up_num
                        #print (u"点赞数: " + str(up_num))

                        # 转发数
                        retweet_num = int(guid[1])
                        self.retweet_num = retweet_num
                        #print (u"转发数: " + str(retweet_num))

                        # 评论数
                        comment_num = int(guid[2])
                        self.comment_num = comment_num
                        #print (u"评论数: " + str(comment_num))

                        dic={
                            'id': self.user_id,
                            '昵称': self.username,
                            '内容': self.weibo_content,
                            '发布时间': self.publish_time,
                            '点赞数': self.up_num,
                            '转发数': self.retweet_num,
                            '评论数': self.comment_num, 
                        }
                        self.save_to_mongo(dic)
        except Exception:
            print("get_weibo_info error")
        
if __name__ == '__main__':
    s = Spider.verify_cookie()
    s.get_weibo_info()