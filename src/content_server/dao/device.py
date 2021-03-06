# -*-coding:utf-8 -*-
import sys
sys.path.append(".")
from mongo import mongo_client
import time
from tornado import log
class DaoDeviceMgr(object):
    def __init__(self):
        self._client = None
        self._client_conn = None
        self._fields = None
        self._client = mongo_client.MongoConnect()
        
        self._fields = ['mac', 'app_name', 'version', 'os', 'hardware','platform']
        self._table = 'device'
    def find_device_by_id(self,id):
        try:
            self._get_conn()
            data={}
            data['_id']=id
            res = self._client_conn[self._table].find(data)
            for item in res:
                if item:
                    return True
                return False
            return False
        except Exception, e:
            log.app_log.info(str(e))
    def _get_conn(self):
        self._client_conn = self._client.get_conn()
        if not self._client_conn:
            raise Exception("connect mongo error")
    
    def insert_device(self, device_info):
        try:
            if not self._check_insert_param(device_info):
                raise Exception("param is invalid")
            
            self._get_conn()   
            data = {}
            data['_id'] = device_info['token']
            self.delete_token(device_info['token'])
            now = time.time()
            data['time']=int(now)
            if "channelid" in device_info:
                data["channelid"]=device_info["channelid"]
            if "group" in device_info:
                data["group"]=device_info["group"]
            #todo, check token exist
            for i in self._fields:
                data[i] = str(device_info[i])
        
            return self._client_conn[self._table].insert(data)
        except Exception, e:
            log.app_log.info(str(e))
            raise e
    def mark_delete_token(self, token):
        try:
            self._get_conn()
            if len(token) == 0:
                raise Exception("token is invalid")
            
            #todo, check token exist
            cond = {}
            cond['_id'] = token
            return self._client_conn[self._table].update(cond, {'$set': {'delete': 1}})
        except Exception, e:
            log.app_log.info(str(e))
        
    def mark_delete_tokens(self, tokens):
        try:
            self._get_conn()
            for token in tokens:
                if len(token) == 0:
                    raise Exception("token is invalid")
                
            cond = {}
            cond['_id'] = {'$in': tokens}
            return self._client_conn[self._table].update_many(cond, {'$set': {'delete': 1}})
        except Exception, e:
            log.app_log.info(str(e))
    
    def delete_tokens(self, tokens):
        try:
            self._get_conn()
            for token in tokens:
                if len(token) == 0:
                    raise Exception("token is invalid")
                
            cond = {}
            cond['_id'] = {'$in': tokens}
            return self._client_conn[self._table].remove(cond)
        except Exception, e:
            log.app_log.info(str(e))
            raise e
    def delete_token(self, token):
        try:
            self._get_conn()
            if len(token) == 0:
                raise Exception("token is invalid")
                
            cond = {}
            cond['_id'] = token
            return self._client_conn[self._table].remove(cond)
        except Exception, e:
            log.app_log.info(str(e))
            raise e
        
    def get_valid_tokens(self):
        try:
            self._get_conn()
            cond = {}
            cond['delete'] = {'$ne': 1}
            return self._client_conn[self._table].find(cond)
        except Exception, e:
            log.app_log.info(str(e))
    def delete_marked_tokens(self):
        try:
            self._get_conn()
            return self._client_conn[self._table].remove({'delete' : 1})
        except Exception, e:
            log.app_log.info(str(e))
               
    def _check_insert_param(self, device_info):
        if not device_info.has_key('token'):
            return False
            
        #if len(device_info['token']) != 64:
            #return False
            
        for i in self._fields:
            if not device_info.has_key(i):
                return False
        
        return True
        
if __name__ == '__main__':
    import test_token
    dao = DaoDeviceMgr()
    print dao.find_device_by_id("38db0bd8f2ff3e8274957d49b0ae21e5c74fd65a06cae0d2d10b0a0ff2caaf5f")
    #device_info = {}
    # device_info['dt'] = '38db0bd8f2ff3e8274957d49b0ae21e5c74fd65a06cae0d2d10b0a0ff2caaf5f'
    # device_info['mac'] = 'fdsfsdf::bd78:21a3:6953:93a5%18'
    # device_info['cl'] = "funshionTV"
    # device_info['ve'] = '1.0.1'
    # device_info['os'] = 'ios9.2'
    # device_info['hardware'] = 'XSDFSD_DSAEFCA_?dwdd'
    # dao.insert_device(device_info)
    
    # device_info = {}
    # device_info['dt'] = 'c5167e16796efb6fc52ccf86b5cebd50d9a2aa1c5e46f20895513df018d79480'
    # device_info['mac'] = 'fdsfsdf::bd78:21a3:6953:93a5%18'
    # device_info['cl'] = "funshionTV"
    # device_info['ve'] = '1.0.1'
    # device_info['os'] = 'ios9.2'
    # device_info['hardware'] = 'XSDFSD_DSAEFCA_?dwdd'
    # dao.insert_device(device_info)
    '''
    for i in range(10):
        device_info['dt'] = test_token.create_token()
        device_info['mac'] = 'fdsfsdf::bd78:21a3:6953:93a5%18'
        device_info['cl'] = "funshionTV"
        device_info['ve'] = '1.0.1'
        device_info['os'] = 'ios9.2'
        device_info['hardware'] = 'XSDFSD_DSAEFCA_?dwdd'
        device_info['msgid']=str(i)
        dao.insert_device(device_info)
    '''
    # tokens = []
    # tokens.append('c5167e16796efb6fc52ccf86b5cebd50d9a2aa1c5e46f20895513df018d79480')
    # tokens.append('38db0bd8f2ff3e8274957d49b0ae21e5c74fd65a06cae0d2d10b0a0ff2caaf5f')
    # dao.delete_tokens(tokens)
        
            
