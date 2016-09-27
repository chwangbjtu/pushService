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
                response["retcode"] = "404"
                response["retmsg"]="error"
            else:
                loadmsg_mgr = loadmsg.DaoLoadMsgMgr()
                res = loadmsg_mgr.get_msg_by_id(msgid)
                for item in res:
                    if "msgid" not in item or "payload" not in item:
                        response["retcode"] = "404"
                        response["retmsg"]="error"
                    else:
                        if "detail" not in item["payload"]: 
                            response["retcode"] = "404"
                            response["retmsg"]="error"
                        else:
                            response["retcode"] = "200"
                            response["retmsg"]="ok"
                            response["msgid"]=msgid
                            response["detail"]=item["payload"]["detail"] 
                    break
                if "retcode" not in response:
                    response["retcode"] = "404"
                    response["retmsg"]="error"
        
        except Exception, e:
            response['retcode'] = "404"
            response['retmsg'] = 'error'
            #log.app_log.info(str(e))
            log.app_log.info(traceback.format_exc())
        
        finally:
            self.write(json.dumps(response))
            
