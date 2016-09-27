# -*-coding:utf-8 -*-
import traceback
from tornado import log
from redis.sentinel import Sentinel

import sys
sys.path.append('.')

#refer: https://pypi.python.org/pypi/redis/
#refer: https://github.com/andymccurdy/redis-py/blob/master/redis/sentinel.py
#refer: https://github.com/andymccurdy/redis-py/blob/master/tests/test_sentinel.py

#有关使用例子，请查看example refer
class SentinelConnect(object):

    def __init__(self, urls, passwd):
        self._sock_timeout = 0.1
        self._urls = urls
        self._passwd = passwd
        self._sentinel = None

        self.connect()

    def connect(self):
        try:
            urls = []
            if self._urls:
                url_tmp = self._urls.split(';')
                for url in url_tmp:
                    ip_port = url.split(':')
                    if len(ip_port) != 2:
                        #只要有一个参数不对，就直接退出
                        return
                    ip = ip_port[0].strip()
                    port = int(ip_port[1].strip())
                    urls.append((ip, port))
            self._sentinel = Sentinel(urls, password=self._passwd, socket_timeout=self._sock_timeout)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #返回(ip, port)
    def discover_master(self, master_name):
        try:
            if not self._sentinel:
                return (None, None)
            return self._sentinel.discover_master(master_name)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #返回[(ip, port)]
    def discover_slaves(self, master_name):
        try:
            if self._sentinel:
                return self._sentinel.discover_slaves(master_name)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #return Redis Client
    def master_for(self, master_name):
        try:
            if self._sentinel:
                return self._sentinel.master_for(master_name, password=self._passwd, socket_timeout=self._sock_timeout)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #return Redis Client
    def slave_for(self, master_name):
        try:
            if self._sentinel:
                return self._sentinel.slave_for(master_name, password=self._passwd, socket_timeout=self._sock_timeout)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":
    passwd = '123456'
    urls = '192.168.16.165:26379'
    master_name = 'shard1'
    sentinel = SentinelConnect(urls, passwd)
    print sentinel.discover_master('shard1')
    master = sentinel.master_for(master_name)
    print master.get('testkey001')
