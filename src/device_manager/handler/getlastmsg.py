# -*-coding:utf-8 -*-
import tornado.web
import sys
sys.path.append(".")
from dao import loadmsg
from tornado import log
import json
import time
import datetime
import traceback
class GetLastMsgHandler(tornado.web.RequestHandler):
    def get_time(self,begin,end):
        try:
            begintime = (datetime.datetime.now()-datetime.timedelta(days=int(begin)))
            endtime = (datetime.datetime.now()-datetime.timedelta(days=int(end)))
            begintime = begintime.strftime("%Y-%m-%d")
            timeArray = time.strptime(begintime, "%Y-%m-%d")
            begintime = int(time.mktime(timeArray))
            endtime = endtime.strftime("%Y-%m-%d")
            timeArray = time.strptime(endtime, "%Y-%m-%d")
            endtime = int(time.mktime(timeArray))
            return (endtime,begintime)
        except Exception,e:
            log.app_log.info(traceback.format_exc())
            return (-1,-1)
    def get(self):  
        response = {}
        try:
            begin = self.get_query_argument('begin', '')
            end = self.get_query_argument('end', '')
            
            if not begin or not end:
                return json.dumps({"retcode":"404","retmsg":"error"})
            if begin > end:
                return json.dumps({"retcode":"404","retmsg":"begin bigger than end."})
                
            loadmsg_mgr = loadmsg.DaoLoadMsgMgr()
            begintime,endtime=self.get_time(begin,end)
            if begintime==-1 or endtime==-1:
                return json.dumps({"retcode":"404","retmsg":"get time error"})
            res = loadmsg_mgr.get_msg_by_day(begintime,endtime)
            msglist = []
            for item in res:
                if "msgid" not in item or "payload" not in item:
                    continue
                if "detail" not in item["payload"]:
                    continue
                dic = {}
                dic["msgid"]=item["msgid"]
                dic["detail"]=item["payload"]["detail"]
                msglist.append(dic)
            response["retcode"] = "200"
            #response["retmsg"]="ok"
            response["msglist"]=msglist
        
        except Exception, e:
            response['retcode'] = "404"
            response['retmsg'] = 'error'
            #log.app_log.info(str(e))
            log.app_log.info(traceback.format_exc())
        
        finally:
            self.write(json.dumps(response))
            
