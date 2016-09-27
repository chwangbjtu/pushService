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
import os
class GetLastMsgHandler(tornado.web.RequestHandler):
    def get_time(self,begin,end):
        try:
            today_time=datetime.datetime.now()
            str_today_time = today_time.strftime("%Y-%m-%d")
            str_today_time = str_today_time+" 23:59:59"
            timeArray = datetime.datetime.strptime(str_today_time, "%Y-%m-%d %H:%M:%S")
            begintime = (timeArray-datetime.timedelta(days=int(begin)))
            endtime = (timeArray-datetime.timedelta(days=int(end)))
            begintime = int(time.mktime(begintime.timetuple()))
            endtime = int(time.mktime(endtime.timetuple()))
            return (endtime,begintime)
        except Exception,e:
            log.app_log.info(traceback.format_exc())
            return (-1,-1)
    def get(self):  
        response = {}
        try:
            begin = self.get_query_argument('begin', '')
            end = self.get_query_argument('offset', '')
            if not begin or not end:
                response['retcode'] = "404"
                response['retmsg'] = 'error'
            elif int(begin) >30:
                response['retcode'] = "404"
                response['retmsg'] = 'error'
            else:
                begin =int(begin)
                if begin <0:
                    begin=0
                end = int(end)
                end = begin+end
                if end >30:
                    end=30
                loadmsg_mgr = loadmsg.DaoLoadMsgMgr()
                if end==begin:
                    response['retcode'] = "200"
                    response['msglist'] = []
                else:
                    begintime,endtime=self.get_time(begin,end)
                    if begintime==-1 or endtime==-1:
                        response['retcode'] = "404"
                        response['retmsg'] = 'error'
                    else:
                        res = None
                        res = loadmsg_mgr.get_msg_by_day(begintime,endtime)
                        msglist = []
                        if not res:
                            response['retcode'] = "404"
                            response['retmsg'] = "error"
                        else:
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
                            response["msglist"]=msglist
        
        except Exception, e:
            response['retcode'] = "404"
            response['retmsg'] = 'error'
            #log.app_log.info(str(e))
            log.app_log.info(traceback.format_exc())
        
        finally:
            self.write(json.dumps(response))
            
