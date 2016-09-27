# -*- coding:utf-8 -*-
import os
import time
import random
import traceback
import socket,fcntl,struct
from tornado import log

import sys
sys.path.append('.')
from conf import Conf
from db.mongo_connect import MongoConnect
from db.mysql_connect import MysqlConnect

class PushMethod(object):
    Push = 'push'
    Pull = 'pull'

class PushType(object):
    All = 'all'
    Test = 'test'

class PushStat(object):
    Finished = 0
    Pushing = 1
    Canceled = 2
    Waiting = 3

class NodeType(object):
    Push = 'push'
    ContentCache = 'content_cache'

class MsgLevel(object):
    Timed = 0
    Instant = 1

#ip:pid:自增值
def create_uuid(increment):
    try:
        ip = get_local_ip('eth0')
        if not ip:
            return
        pid = os.getpid() 
        if not pid:
            return
        if not increment:
            return
        return '%s:%s:%s' % (ip, pid, increment)
    except Exception, e:
        log.app_log.error(traceback.format_exc())

def create_id():
    res = 1
    try:
        res = random.randint(1, sys.maxint)                
    except Exception, e:
        res = 0
        log.app_log.error(traceback.format_exc())
    finally:
        return res

def get_local_ip(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
        ret = socket.inet_ntoa(inet[20:24])
        return ret
    except Exception, e:
        log.app_log.error(traceback.format_exc())

def timestamp2datetime(timestamp):
    try:
        time_stamp = time.localtime(timestamp) 
        time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time_stamp)
        return time_stamp
    except Exception, e:
        log.app_log.error(traceback.format_exc())

def check_mongo():
    res = True
    try:
        mongo = MongoConnect(Conf.mg_urls, Conf.mg_db, Conf.mg_user, Conf.mg_passwd) 
        if mongo.is_connected(): 
            res = True
        else:
            res = False
    except Exception, e:
        res = False
        log.app_log.error(traceback.format_exc())
    finally:
        return res

def check_mysql():
    res = True
    try:
        mysql = MysqlConnect(host=Conf.sql_host, port=Conf.sql_port, user=Conf.sql_user, passwd=Conf.sql_passwd, db=Conf.sql_db)
        if mysql.is_connected(): 
            res = True
        else:
            res = False
    except Exception, e:
        res = False
        log.app_log.error(traceback.format_exc())
    finally:
        return res

if __name__ == '__main__':
    print get_local_ip('eth0')
    print check_mongo()
    print check_mysql()
