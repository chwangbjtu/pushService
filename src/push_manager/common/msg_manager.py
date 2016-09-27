# -*- coding:utf-8 -*-
import time
import pymongo
import traceback
from tornado import log

import sys
sys.path.append('.')
from conf import Conf
from common.util import PushMethod, MsgLevel
from db.mongo_connect import MongoConnect

'''
消息管理
    历史消息队列        msg_history(msgid)
        所有推送消息记录，都放在该列表中
        msgid, start_time, msg_type, msg_level, payload
    等待推送队列        msg_waiting
        msg_waiting_push
        msg_waiting_pull
        还未开始推送的所有消息记录 
        msgid, start_time, msg_type, msg_level, payload
        取消推送时，删除
    正在推送token列表   msg_token
        msg_token_push
        msgid
        只有msgid
        msg_token_pull(app_name)
        msgid, app_name, token
        token以basic_num为一簇，这样方便弹出
    进度结果队列        msg_progress(msgid)
        记录msg的推送进度
        msgid, stat
        total, success, fail: 这三个字段，由于没有推送结束状态，所以不用
        取消推送时，更新状态
    进度上报详情队列    msg_progress_detail(msgid, reportid)
        msgid, reportid, total, success, fail
    个性化token队列     token_custom
        msgid, token
'''
class MsgManager(object):

    def __init__(self):
        self._mongo = MongoConnect(Conf.mg_urls, Conf.mg_db, Conf.mg_user, Conf.mg_passwd) 

    '''
    msg_history
    '''
    def findone_msg_history_by_msgid(self, msgid):
        res = None
        try:
            coll_name = 'msg_history'
            res = self._mongo.find_one(coll_name, {"msgid":msgid})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def insertone_msg_history(self, msg):
        res = None
        try:
            coll_name = 'msg_history'
            res = self._mongo.insert_one(coll_name, msg)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res
    
    def deleteone_msg_history(self, msg):
        res = None
        try:
            coll_name = 'msg_history'
            res = self._mongo.delete_one(coll_name, filter={'msgid':msg['msgid'], 'start_time':msg['start_time']})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    '''
    msg_waiting
    '''
    def getone_msg_waiting(self, method):
        res = None
        try:
            res = self.findone_and_delete_msg_waiting(method=method, msg_level=MsgLevel.Instant)
            if not res:
                res = self.findone_and_delete_msg_waiting(method=method, msg_level=MsgLevel.Timed)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def findone_and_delete_msg_waiting(self, method, msg_level=None):
        res = None
        try:
            coll_name = None
            if method == PushMethod.Push:
                coll_name = 'msg_waiting_push'
            elif method == PushMethod.Pull:
                coll_name = 'msg_waiting_pull'
            if not coll_name:
                return
            now = int(time.time()) 
            if msg_level == MsgLevel.Timed:
                res = self._mongo.find_one_and_delete(coll_name, filter={"msg_level":msg_level, "start_time":{"$lte":now}}, sort=[('start_time',pymongo.ASCENDING)])
            elif msg_level == MsgLevel.Instant:
                res = self._mongo.find_one_and_delete(coll_name, filter={"msg_level":msg_level}, sort=[('start_time',pymongo.ASCENDING)])
            else:
                res = self._mongo.find_one_and_delete(coll_name, filter={"start_time":{"$lte":now}}, sort=[('start_time',pymongo.ASCENDING)])
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def insertone_msg_waiting(self, method, msg):
        res = None
        try:
            coll_name = None
            if method == PushMethod.Push:
                coll_name = 'msg_waiting_push'
            elif method == PushMethod.Pull:
                coll_name = 'msg_waiting_pull'
            if not coll_name:
                return
            res = self._mongo.insert_one(coll_name, msg)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def deletemany_msg_waiting_by_msgid(self, method, msgid):
        res = None
        try:
            coll_name = None
            if method == PushMethod.Push:
                coll_name = 'msg_waiting_push'
            elif method == PushMethod.Pull:
                coll_name = 'msg_waiting_pull'
            if not coll_name:
                return
            res = self._mongo.delete_many(coll_name, filter={'msgid':msgid})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res


    '''
    msg_token
    '''
    def getone_msg_token(self, method):
        res = None
        try:
            coll_name = None
            if method == PushMethod.Push:
                coll_name = 'msg_token_push'
            elif method == PushMethod.Pull:
                coll_name = 'msg_token_pull'
            if not coll_name:
                return
            res = self._mongo.find_one(coll_name)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res
    
    def popone_msg_token(self, method): 
        res = None
        try:
            coll_name = None
            if method == PushMethod.Push:
                coll_name = 'msg_token_push'
                res = self._mongo.find_one_and_delete(coll_name, filter={})
            elif method == PushMethod.Pull:
                coll_name = 'msg_token_pull'
                res = self._mongo.find_one_and_delete(coll_name, filter={}, sort=[('app_name',pymongo.ASCENDING)])
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def pushone_msg_token(self, method, msg_token):
        res = None
        try:
            coll_name = None
            if method == PushMethod.Push:
                coll_name = 'msg_token_push'
            elif method == PushMethod.Pull:
                coll_name = 'msg_token_pull'
            if not coll_name:
                return
            res = self._mongo.insert_one(coll_name, msg_token)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def deletemany_msg_token(self, method, msgid):
        res = None
        try:
            coll_name = None
            if method == PushMethod.Push:
                coll_name = 'msg_token_push'
            elif method == PushMethod.Pull:
                coll_name = 'msg_token_pull'
            if not coll_name:
                return
            res = self._mongo.delete_many(coll_name, filter={'msgid':msgid})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res


    '''
    msg_progress
    '''
    def getone_msg_progress_by_msgid(self, msgid): 
        res = None
        try:
            prog = self.findone_msg_progress_by_msgid(msgid) 
            if not prog:
                return res
            stat = int(prog['stat'])
            proges = self.find_msg_progress_detail_by_msgid(msgid)
            total=0; success=0; fail=0;
            if not proges:
                res = {'stat':stat, 'total':total, 'success':success, 'fail':fail}    
                return res
            for prog in proges: 
                total = total + int(prog['total'])
                success = success + int(prog['success'])
                fail = fail + int(prog['fail'])
            res = {'stat':stat, 'total':total, 'success':success, 'fail':fail}    
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def findone_msg_progress_by_msgid(self, msgid):
        res = None
        try:
            coll_name = 'msg_progress'
            res = self._mongo.find_one(coll_name, {'msgid':msgid})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def update_or_insert_msg_progress(self, msg_progress):
        res = None
        try:
            coll_name = 'msg_progress'
            msgid = msg_progress['msgid']
            res = self._mongo.find_one_and_update(coll_name, filter={"msgid":msgid}, update={'$set':msg_progress}, upsert=True, return_document=1)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    
    '''
    msg_progress_detail 
    '''
    #查找一个记录，若存在则更新，不存在，则插入
    def update_or_insert_msg_progress_detail(self, msg_progress_detail):
        res = None
        try:
            coll_name = 'msg_progress_detail'
            msgid = msg_progress_detail['msgid']
            reportid = msg_progress_detail['reportid']
            res = self._mongo.find_one_and_update(coll_name, filter={"msgid":msgid, "reportid":reportid}, update={'$set':msg_progress_detail}, upsert=True, return_document=1)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    #根据msgid获取消息推送的进度 
    def find_msg_progress_detail_by_msgid(self, msgid):
        res = []
        try:
            coll_name = 'msg_progress_detail'
            result = self._mongo.find(coll_name, filter={'msgid':msgid})
            for rs in result:
                try:
                    tmp = {'msgid':rs['msgid'], 'reportid':rs['reportid'], 'total':rs['total'], 'success':rs['success'], 'fail':rs['fail']}
                    res.append(tmp)
                except Exception, e:
                    log.app_log.error(traceback.format_exc())
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def deletemany_msg_progress_detail_by_msgid(self, msgid):
        res = []
        try:
            coll_name = 'msg_progress_detail'
            res = self._mongo.delete_many(coll_name, filter={'msgid':msgid})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res


    '''
    token_custom
    '''
    def insertone_token_custom(self, token_custom):
        res = None
        try:
            coll_name = 'token_custom'
            res = self._mongo.insert_one(coll_name, token_custom)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def findone_token_custom_by_msgid(self, msgid):
        res = None
        try:
            coll_name = 'token_custom'
            res = self._mongo.find_one(coll_name, {"msgid":msgid})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def deletemany_token_custom_by_msgid(self, msgid):
        res = None
        try:
            coll_name = 'token_custom'
            res = self._mongo.delete_many(coll_name, filter={'msgid':msgid})
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res


if __name__ == '__main__':
    test = MsgManager()
    #msgid = '1112233501'
    msgid = '11111111'
    res = test.findone_msg_progress_by_msgid(msgid)
    print res
