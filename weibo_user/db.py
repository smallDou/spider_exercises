from redis import Redis
from settings import *
from pymongo import MongoClient

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        if REDIS_PASSWORD:
            self._db = Redis(host=host, port=port, db=1, password=REDIS_PASSWORD)
        else:
            self._db = Redis(host=host, port=port, db=1)
        
        ##获取最后一个元素的source
        if self._db.zrange('cookies',0,0,desc=True):
            for i in self._db.zrange('cookies',0,0,desc=True):
                self._source = self._db.zscore('cookies',i) + 1
        else:
            self._source = 1

    def add(self,dic):
        self._db.zadd('cookies',dic,self._source)
        self._source+=1
    
    def get(self):
        for i in self._db.zrange('cookies',0,0,desc=False,withscores=False):
            return eval(i.decode('utf-8'))
    
    def add_score(self,dic):
        local_score = self._db.zscore('cookies',dic)
        print(local_score)
        if local_score:
            if local_score<100:
                #zincrby后面的数值为添加
                self._db.zincrby('cookies',dic,10)
            else :
                self.delete(dic)

    def delete(self,dic):
        self._db.zrem('cookies',dic)

    def print(self):
        print(self._db.zrange('cookies',0,-1,desc=False,withscores=True))


class MongoDB(object):
    def __init__(self,host=MONGO_HOST,port=MONGO_PORT):
        self._client = MongoClient(MONGO_HOST,MONGO_PORT)
        self._db = self._client['weibo']
        self._collection = self._db['weibo'] 
    
    def insert(self,dic):
        self._collection.insert(dic)
    
    #判断数据是否存在
    def find(self,dic):
        return self._collection.find_one(dic)

if __name__ == '__main__':
    mon = MongoDB()
    dic = {'name':'test','name2':'test'}
    mon.insert(dic)
    dic2 = {'name':'test'}
    print(mon.find(dic2))
    
