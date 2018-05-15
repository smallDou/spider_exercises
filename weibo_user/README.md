# 实时爬取某用户微博
## Python
python3.X
## 启动方式
```
python run.py
```
## 说明
+ run.py 程序入口
+ login.py 获取cookie，并存入redis
+ spider.py 从redis获取cookie，爬取想要数据；数据存入mongodb，存储过程检测是否存在，不存在则爬取，存在则不处理
+ db.py 处理redis、mongodb
+ settings.py 配置文件

## **Stttings.py 配置**
```
## 登录
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