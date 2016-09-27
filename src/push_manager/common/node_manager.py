# -*- coding:utf-8 -*-
import traceback
from tornado import log

import sys
sys.path.append('.')
from conf import Conf
from db.mongo_connect import MongoConnect

'''
节点管理
    节点队列        node(ip, type)
    ip, type( ,port)
'''
class NodeManager(object):

    def __init__(self):
        self._mongo = MongoConnect(Conf.mg_urls, Conf.mg_db, Conf.mg_user, Conf.mg_passwd) 

    #增加节点
    def update_or_insert_node(self, type, ip):
        res = None
        try:
            if ip and type:
                coll_name = 'node'
                node = {'ip':ip, 'type':type}
                res = self._mongo.find_one_and_update(coll_name, filter={'ip':ip, 'type':type}, update={'$set': node}, upsert=True, return_document=1)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    #删除节点
    def deletemany_node(self, type=None, ip=None):
        res = None
        try:
            coll_name = 'node'
            filter = {}
            if ip:
                filter['ip'] = ip
            if type:
                filter['type'] = type
            res = self._mongo.delete_many(coll_name, filter=filter)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    #查询节点
    def findmany_node(self, type=None, ip=None):
        res = []
        try:
            coll_name = 'node'
            filter = {}
            if ip:
                filter['ip'] = ip
            if type:
                filter['type'] = type
            result = self._mongo.find(coll_name, filter=filter)
            for rs in result:
                try:
                    tmp = {'ip':rs['ip'], 'type':rs['type']}
                    res.append(tmp)
                except Exception, e:
                    log.app_log.error(traceback.format_exc())
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res
