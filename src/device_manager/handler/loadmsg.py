# -*-coding:utf-8 -*-
import tornado.web
import sys
sys.path.append(".")
from dao import loadmsg
from tornado import log
import json
import traceback
class LoadMsgHandler(tornado.web.RequestHandler):           
    def get(self):  
        response = {}
        try:
            msgid = self.get_query_argument('msgid', '')
            if not msgid:
                return json.dumps({"retcode":"404","retmsg":"error"})
            loadmsg_mgr = loadmsg.DaoLoadMsgMgr()
            res = loadmsg_mgr.get_msg_by_id(msgid)    
            if "msgid" not in res[0] or "payload" not in res[0]:
                return json.dumps({"retcode":"404","retmsg":"error"})
            if "detail" not in res[0]["payload"]:
                return json.dumps({"retcode":"404","retmsg":"error"})
            response["retcode"] = "200"
            response["retmsg"]="ok"
            response["msgid"]=msgid
            response["detail"]=res[0]["payload"]["detail"]
        
        except Exception, e:
            response['retcode'] = "404"
            response['retmsg'] = 'error'
            #log.app_log.info(str(e))
            log.app_log.info(traceback.format_exc())
        
        finally:
            self.write(json.dumps(response))
            
