# -*- coding: utf-8 -*-
import pymysql
from setting import *

class MysqlClient():
    def __init__(self,user=user,passwd=passwd,host=host,db=db):
        self.conn = pymysql.connect(user=user, passwd=passwd,
                 host=host, db=db,charset='utf8')
        self.cur = self.conn.cursor()

    #增
    def add(self,query,title,url):  
        sql = "insert into wechat (query, title,url) values (%s, %s,%s)"  
        param = (query, title,url)  
        n = self.cur.execute(sql, param)
        #print "添加成功"   
        self.conn.commit()  

if __name__ == '__main__':
    m = MysqlClient()
    m.add('test','test','test')

