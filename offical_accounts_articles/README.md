# 抓取某微信公众号全部文章
## Python
python3.X
## 启动方式
```
python run.py
```
## 说明
+ run.py 程序入口，cookie失效需要手动运行login.py扫码登录
+ login.py 获取cookie，并存入cookie.txt（也可以选择存入redis）
+ spider.py 从cookie.py获取cookie，爬取某公众号全部文章链接
+ db.py 处理redis、mongodb
+ settings.py 配置文件

## **Stttings.py 配置**
```
## 登录,必须有微信公众号账号，没有可以去https://mp.weixin.qq.com/注册订阅号
USERNAME = ''
PASSWORD = ''

##redis地址和端口,用于储存cookie
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

##mongo地址和端口，用于存储数据
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
```