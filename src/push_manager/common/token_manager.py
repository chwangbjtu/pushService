# -*- coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.')
from conf import Conf
from db.mongo_connect import MongoConnect

'''
token管理
'''
class TokenManager(object):

    def __init__(self):
        self._mongo = MongoConnect(Conf.mg_urls, Conf.mg_db, Conf.mg_user, Conf.mg_passwd) 
        self._find_batch_size = 100000

    def find_token_ios(self):
        res = []
        try:
            appname = self.find_appname_ios()
            if not appname:
                return res
            for an in appname:
                token = self.find_token_by_appname_ios(an)
                res = res + token
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def find_appname_ios(self):
        res = []
        try:
            coll_name = 'device'
            res = self._mongo.distinct(coll_name, key='app_name', filter={'platform':'ios'})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def find_token_by_appname_ios(self, app_name):
        res = []
        try:
            coll_name = 'device'
            result = self._mongo.find(coll_name, filter={'app_name':app_name}, projection={'_id':True}, find_batch_size=self._find_batch_size)
            count = 0
            token = []
            for rs in result:
                try:
                    count = count + 1 
                    #ObjectId("53b3a89bf988c39955a30f9e") -> 53b3a89bf988c39955a30f9e 
                    #id = str(rs['_id'])
                    token.append(rs['_id'])
                    if count == Conf.token_basic_number:
                        res.append({"app_name":app_name, "token":token})
                        count = 0
                        token = []
                except Exception, e:
                    log.app_log.error(traceback.format_exc())
            #最后几个
            if token:
                res.append({"app_name":app_name, "token":token})
                count = 0
                token = []
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

if __name__ == '__main__':
    test = TokenManager()
    res = test.find_token_ios()
    print res
