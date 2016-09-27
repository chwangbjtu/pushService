#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
import sys

#host = '192.168.177.3'
#pwd = 'funshion'
#user = 'root'
#db = 'ch_old'
#port = 3306

def write_into_mysql(sql, charset = 'utf8'):
            try:
                conn = MySQLdb.connect(host='192.168.177.3', user='root', passwd='funshion', db='ch_old')
                cursor = conn.cursor()
                #print cursor
                cursor.execute("select * from blacklist")
                cursor.execute("set NAMES utf8")
                #print "1"
                cursor.execute(sql)
                #print '2'
                cursor.execute("select * from blacklist")
                conn.commit()
                cursor.close()
                conn.close()
            except Exception, e:
                print 'write_into_mysql：第 ' + str(sys._getframe().f_lineno) + ' 行报错', e
                print sys.exc_info()
                
def insert_db():
    bls = file('black_list.txt')
    for bl in bls:
        #print bl[:-1]
        sql = "insert into blacklist (word) values (\'%s\'); "%(bl[:-1])
        #print sql
        write_into_mysql(sql)
        #break
'''
def la():
    try:
        conn = MySQLdb.connect(host='192.168.177.3', user='root', passwd='funshion', db='ch_old',charset="utf8")
        cursor = conn.cursor()
        #print cursor
        cursor.execute("select * from blacklist")
        cursor.execute("set NAMES utf8")
        #print "1"
        bls = open('black_list.txt')
        for bl in bls:
            #print bl[:-1]
            sql = "INSERT INTO blacklist(word) VALUES (\'%s\'); "%bl[:-1].encode('utf8')
            sql1 = "select count(*) from blacklist "
            print sql           
            print cursor.execute(sql1)
            break
        #print '2'
        cursor.execute("select * from blacklist")
        print cursor.fetchall()
        conn.close()
    except Exception, e:
        print 'write_into_mysql：第 ' + str(sys._getframe().f_lineno) + ' 行报错', e
        print sys.exc_info()
'''

if __name__ == "__main__":
    insert_db()
    #la()
