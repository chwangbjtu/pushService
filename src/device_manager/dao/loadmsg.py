# -*-coding:utf-8 -*-
import sys
sys.path.append(".")
from mongo import mongo_client
import time
class DaoLoadMsgMgr(object):
    def __init__(self):
        self._client = None
        self._client_conn = None
        self._fields = None
        self._client = mongo_client.MongoConnect()
        
        self._fields = ["msg_id","start_time","payload"]
        self._table = 'msg_history'
        
    def _get_conn(self):
        self._client_conn = self._client.get_conn()
        if not self._client_conn:
            raise Exception("connect mongo error")
        
    def get_msg_by_id(self,msgid):
        self._get_conn()
        cond = {}
        cond['msgid'] = msgid
        return self._client_conn[self._table].find(cond)
    def get_msg_by_day(self,begin,end):
        self._get_conn()
        cond={"msg_type":"all","start_time":{"$gte":begin,"$lte":end}}
        return self._client_conn[self._table].find(cond)
    def insert_data(self,data):
        self._get_conn()
        self._client_conn[self._table].insert(data)

if __name__ == '__main__':
    import test_token
    dao = DaoLoadMsgMgr()
    ''' 
    c = dao.get_msg_by_id("1")
    for item in c:
        print item
    '''
    t = '2015-12-%s 12:54:29'
    for i in range(29):
        data ={}
        tmp = t%str(i+1)
        timeArray = time.strptime(tmp, "%Y-%m-%d %H:%M:%S")
        data['start_time']=int(time.mktime(timeArray))
        data["msgid"]=str(i)
        data["payload"]="this is the %s test msg" % str(i)
        data["msg_type"]="all"
        dao.insert_data(data)
    '''
    c = dao.get_msg_by_day("2015-12-2 12:54:29","2015-12-9 12:54:29")
    for item in c:
        print item
    '''
