# -*-coding:utf-8 -*-
import time
import redis
import traceback
from tornado import log
from redis.exceptions import ConnectionError
from redis.sentinel import MasterNotFoundError, SlaveNotFoundError 

import sys
sys.path.append('.')

#refer: http://doc.redisfans.com/
#refer: https://kushal.fedorapeople.org/redis-py/html/api.html
#refer: https://github.com/andymccurdy/redis-py/blob/master/redis/client.py
#example refer: https://github.com/andymccurdy/redis-py/blob/master/tests/test_commands.py

#有关使用例子，请查看example refer
class RedisConnect(object):

    #两种方式构建RedisConnect
        #一种传统的host, port, password方式
        #另一种利用Sentinel.master_for返回的StrictRedis来初始化RedisConnect
    def __init__(self, host='', port='', passwd='', redis=None):
        self._host = host
        self._port = port
        self._passwd = passwd
        self._redis = redis
        self._retry_times = 3

        self.connect()

    def connect(self):
        try:
            if self._redis:
                pass
            elif self._host and self._port:
                self._redis = redis.Redis(host=self._host, port=self._port, db=0, password=self._passwd)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def check_connected(self):
        res = False
        cnt = 0
        while cnt < self._retry_times:
            try:
                if self._redis and self._redis.ping():
                    res = True
                    break
                else:
                    self.connect()
                    pass
            except ConnectionError, err:
                log.app_log.error(traceback.format_exc())
                time.sleep(0.3)
            except MasterNotFoundError, err:
                log.app_log.error(traceback.format_exc())
                time.sleep(0.3)
            except SlaveNotFoundError, err:
                log.app_log.error(traceback.format_exc())
                time.sleep(0.3)
            except Exception, err:
                log.app_log.error(traceback.format_exc())
            finally:
                cnt = cnt + 1
        return res

    #key
    #设置过期时间
    def expire(self, name, time):
        try:
            if not self.check_connected():
                return
            return self._redis.expire(name, time)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #设置过期时间戳
    def expireat(self, name, when):
        try:
            if not self.check_connected():
                return
            return self._redis.expireat(name, when)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def delete(self, *names):
        try:
            if not self.check_connected():
                return
            return self._redis.delete(*names)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def exists(self, *names):
        try:
            if not self.check_connected():
                return
            return self._redis.exists(*names)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def keys(self, pattern='*'):
        try:
            if not self.check_connected():
                return
            return self._redis.keys(pattern)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #string
    def get(self, name):
        try:
            if not self.check_connected():
                return
            return self._redis.get(name)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    获取多个值
    '''
    def mget(self, keys, *args):
        try:
            if not self.check_connected():
                return
            return self._redis.mget(keys, *args)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        try:
            if not self.check_connected():
                return
            return self._redis.set(name, value, ex, px, nx, xx)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    不更新地添加
    '''
    def setnx(self, name, value):
        try:
            if not self.check_connected():
                return
            return self._redis.setnx(name, value)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    支持更新与不更新地设置多个值
    '''
    def mset(self, update=True, *args, **kwargs):
        try:
            if not self.check_connected():
                return
            if update:
                return self._redis.mset(*args, **kwargs)
            else:
                return self._redis.msetnx(*args, **kwargs)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def setex(self, name, time, value):
        try:
            if not self.check_connected():
                return
            return self._redis.setex(name, time, value)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #sorted set
    #_redis.zadd('waitting_msg', '001:1990', 10)
    #dct = {'002:1991':11}  _redis.zadd('waitting_msg', **dct)
    def zadd(self, name, *args, **kwargs):
        try:
            if not self.check_connected():
                return
            return self._redis.zadd(name, *args, **kwargs)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
    
    def zscan(self, name, cursor=0, match=None, count=None, score_cast_func=float):
        try:
            if not self.check_connected():
                return
            return self._redis.zscan(name, cursor, match, count, score_cast_func)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def zrem(self, name, *values):
        try:
            if not self.check_connected():
                return
            return self._redis.zrem(name, *values) 
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    此处下标sorted sort的成员以score升序排序
    start, end:返回sorted sort中[start, end]的数据 
    desc:返回的结果集以升/降序排列
    withscores:是否同时返回score
    '''
    def zrange(self, name, start, end, desc=False, withscores=False, score_cast_func=float):
        try:
            if not self.check_connected():
                return
            return self._redis.zrange(name, start, end, desc, withscores, score_cast_func)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def zrangebyscore(self, name, min, max, start=None, num=None, withscores=False, score_cast_func=float): 
        try:
            if not self.check_connected():
                return
            return self._redis.zrangebyscore(name, min, max, start, num, withscores, score_cast_func)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    注意此处下标sorted sort的成员以score降序排序
    start, end:返回sorted sort中[start, end]的数据 
    withscores:是否同时返回score
    '''
    def zrevrange(self, name, start, end, withscores=False, score_cast_func=float):
        try:
            if not self.check_connected():
                return
            return self._redis.zrevrange(name, start, end, withscores, score_cast_func)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def zrevrangebyscore(self, name, max, min, start=None, num=None, withscores=False, score_cast_func=float):
        try:
            if not self.check_connected():
                return
            return self._redis.zrevrangebyscore(name, min, max, start, num, withscores, score_cast_func)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def pop(self, name, withscores=True):
        try:
            if not self.check_connected():
                return
            result = self.zrange(name, 0, 0, withscores=withscores)
            if not result:
                return
            #返回第0个
            if withscores:
                result = result[0]
                member = result[0]
            else:
                member = result[0]
            if self.zrem(name, member): 
                return member
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #list
    def llen(self, name):
        try:
            if not self.check_connected():
                return
            return self._redis.llen(name)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def lpop(self, name): 
        try:
            if not self.check_connected():
                return
            return self._redis.lpop(name)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def rpush(self, name, *values):
        try:
            if not self.check_connected():
                return
            return self._redis.rpush(name, *values)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def rpushx(self, name, value):
        try:
            if not self.check_connected():
                return
            return self._redis.rpushx(name, values)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #hash
    #返回给定name的所有keys
    def hkeys(self, name):
        try:
            if not self.check_connected():
                return
            return self._redis.hkeys(name)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #给定的key(field)是否存在
    def hexists(self, name, key): 
        try:
            if not self.check_connected():
                return
            return self._redis.hexists(name, key)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def hget(self, name, key):
        try:
            if not self.check_connected():
                return
            return self._redis.hget(name, key)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    Return:
        {'total': '100', 'stat': '0', 'msg_id': '1'}
    '''
    def hgetall(self, name):
        try:
            if not self.check_connected():
                return
            return self._redis.hgetall(name)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def hset(self, name, key, value):
        try:
            if not self.check_connected():
                return
            return self._redis.hset(name, key, value)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #不更新地添加
    def hsetnx(self, name, key, value):
        try:
            if not self.check_connected():
                return
            return self._redis.hsetnx(name, key, value)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    #同时设置多个field的值
    def hmset(self, name, mapping):
        try:
            if not self.check_connected():
                return
            return self._redis.hmset(name, mapping)
        except Exception, err:
            log.app_log.error(traceback.format_exc())


if __name__ == "__main__":
    from sentinel_connect import SentinelConnect
    passwd = '123456'
    urls = '192.168.16.165:26379'
    master_name = 'freyr'
    sentinel = SentinelConnect(urls, passwd)
    master = sentinel.master_for(master_name)
    redis_2 = RedisConnect(redis=master)
    value = '{"token": [], "app_name": "ipad"}'
    redis_2.rpush('msg_token_pull:test', value)
