# -*- coding:utf-8 -*-
import json
import redis
from pymongo import MongoClient
#import traceback
#from tornado import log
import sys
#sys.path.append('.')
#from conf import Conf
#from db.mongo_connect import MongoConnect
'''
token管理
'''

class MongoConnect(object):
    def __init__(self, urls, db, user, passwd):
        self._urls = urls
        self._dbname = db
        self._username = user
        self._passwd = passwd
        self.connect()
    def connect(self):
        try:
            urls = []
            if self._urls:
                url_tmp = self._urls.split(';')
                for url in url_tmp:
                    url = url.strip()
                    urls.append(url)
            self._mongo = MongoClient(urls)
            self._db = getattr(self._mongo, self._dbname)
            self._db.authenticate(self._username, self._passwd)
        except Exception, err:
            print err
            #log.app_log.error(traceback.format_exc())

    def distinct(self, coll_name, key, filter=None, **kwargs):
        try:
            if self._db:
                return self._db[coll_name].distinct(key, filter, **kwargs)
        except Exception, err:
            print err
            #log.app_log.error(traceback.format_exc())

    def find(self, coll_name, filter=None, projection=None, skip=0, limit=0, sort=None, allow_partial_results=False, find_batch_size=0):
        try:
            if self._db:
                if find_batch_size > 0:
                    return self._db[coll_name].find(filter=filter, projection=projection, skip=skip, limit=limit, sort=sort, allow_partial_results=allow_partial_results).batch_size(find_batch_size)
                else:
                    return self._db[coll_name].find(filter=filter, projection=projection, skip=skip, limit=limit, sort=sort, allow_partial_results=allow_partial_results)
        except Exception, err:
            print err
            #log.app_log.error(traceback.format_exc())

class TokenManager(object):
    def __init__(self):
        self._mongo = MongoConnect("192.168.16.165:27017", "xv", "xv", "xv") 
        #self._mongo = MongoConnect(Conf.mg_urls, Conf.mg_db, Conf.mg_user, Conf.mg_passwd) 
        self._find_batch_size = 100000

    def get_all_token(self):
        res = []
        try:
            appname = []
            coll_name = 'device'
            appname = self._mongo.distinct(coll_name, key='app_name', filter={'platform':'ios'})
            print appname
            if not appname:
                return res
            for an in appname:
                coll_name = 'device'
                result = self._mongo.find(coll_name, filter={'app_name':an}, projection={'_id':True}, find_batch_size=self._find_batch_size)
                token = []
                for rs in result:
                    #ObjectId("53b3a89bf988c39955a30f9e") -> 53b3a89bf988c39955a30f9e 
                    #id = str(rs['_id'])
                    token.append(rs['_id'])
                res.append({"app_name":an, "token":token})
        except Exception, e:
            print e
            #log.app_log.error(traceback.format_exc())
        finally:
            return res

class RedisTokenCleaner(object):
    def __init__(self):
        #redis_con = redis.StrictRedis(host=db_host, port=db_port, db=0)
        self.redis_con = redis.StrictRedis(host="192.168.16.113", port=6379, db=0)

    #toekn_info_list is:[{'token': [u'2b0dec5ceb8ab71aeba3cd42a3f14dd5863436cd53dc6ddfe1a609dbc9430c'], 'app_name': u'iphone'}]
    def clean(self,token_info_list):
        try:
            for item in token_info_list:
                app_name = item["app_name"]
                for titem in item["token"]:
                    name = "push:%s:%s:devicetoken_json_string" % (app_name,titem)
                    try:
                        values = self.redis_con.get(name)
                        if values:
                            self.redis_con.delete(name)
                            zname = "push:%s:devicetoken_zset" % app_name
                            self.redis_con.zrem(zname,titem)
                    except Exception, e:
                        print e
        except Exception, e:
            print e
        finally:
            pass

if __name__ == '__main__':
    test = TokenManager()
    rc = RedisTokenCleaner()
    res = test.get_all_token()
    print len(res)
    rc.clean(res)
