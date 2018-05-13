import redis
from settings import REDIS_HOST,REDIS_PASSWORD,REDIS_PORT

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        if REDIS_PASSWORD:
            self._db = redis.Redis(host=host, port=port, db=1, password=REDIS_PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port, db=1)
        
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
        return self._db.zrange('cookies',0,0,desc=False,withscores=False)
    
    def add_score(self,dic):
        local_score = self._db.zscore('cookies',dic)
        print(local_score)
        if local_score:
            #zincrby后面的数值为添加
            self._db.zincrby('cookies',dic,2) 

    def delete(self,dic):
        self._db.zrem('cookies',dic)

    def print(self):
        print(self._db.zrange('cookies',0,-1,desc=False,withscores=True))

if __name__ == '__main__':
    conn = RedisClient()
    dic = {'niha':'test'}
    conn.delete(dic)
    conn.print()
    
