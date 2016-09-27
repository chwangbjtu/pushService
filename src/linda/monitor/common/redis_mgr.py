# -*-coding:utf-8 -*-
import traceback
from tornado import log
import redis

import sys
sys.path.append('.')
from common.conf import Conf

class RedisMgr(object):
    def __init__(self):
        self._redis = redis.Redis(host=Conf.redis_host, port=Conf.redis_port, db=0, password=Conf.redis_passwd)

    def check_connected(self):
        res = False
        try:
            cnt = 1
            while cnt < 50:
                if self._redis.ping():
                    res = True
                    break
                else:
                    cnt += cnt
                    self._redis = redis.Redis(host=cs.redis_ip, port=cs.redis_port, db=0,password=cs.redis_pwd)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
        return res

    def get_count(self, key):
        try:
            if self.check_connected() and key:
                return self._redis.zcard(key)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
    
if __name__ == "__main__":
    redis_mgr = RedisMgr()
    print redis_mgr.get_count('mz_q')
