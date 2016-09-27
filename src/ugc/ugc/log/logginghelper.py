#!/usr/bin/python
# -*- coding:utf-8 -*- 
import os
import masterlogging
import utils

#prevent the confict between the info string with csv format
def encode_csv_info(src):
    return src.replace(',','##')

def contact_list_items(items):
    if len(items) == 1:
        return str(items)
    result = ""
    for item in items:
        if result != "":
            result += "+%s" % str(item)
        else:
            result = str(item)
    return result

class LoggingHelper(object):
    LOG_TYPE_SYS = "system"
    LOG_TYPE_LOGIC = "business"
    LOG_TYPE_MGMT = "mgmt"
    
    @staticmethod
    def packLogicLog(tid,operation,result,info):
        return "%s,%s,%s,%s,%s" % (LoggingHelper.LOG_TYPE_LOGIC,tid,operation,result,encode_csv_info(info))

    @staticmethod
    def packSystemLog(posinfo,apiname,errinfo):
        filename,lineno = (posinfo[0],posinfo[1])
        return "%s,%s,%s,%s,%s" % (LoggingHelper.LOG_TYPE_SYS,filename,str(lineno),apiname,encode_csv_info(errinfo))

    @staticmethod
    def packMgmtLog(sourceip,url,request_body,response):
        return "%s,%s,%s,%s,%s" % (LoggingHelper.LOG_TYPE_MGMT,sourceip,url,encode_csv_info(request_body),encode_csv_info(response))

def LogicLog(who,operation,result,info):
    return LoggingHelper.packLogicLog(who,operation,result,info)
def SystemLog(posinfo,apiname,errinfo):
    return LoggingHelper.packSystemLog(posinfo,apiname,errinfo)
def MgmtLog(sourceip,url,request_body,response):
    return LoggingHelper.packMgmtLog(sourceip,url,request_body,response)

#code below is just for testing
if __name__ == "__main__":
    masterlogging.initialize("log",output_to_console = "false")
    masterlogging.warn(MgmtLog("192.168.16.34","http://master.com:8888/get_task","None",'{"result":"ok"}'))
    masterlogging.info(MgmtLog("192.168.16.35","http://master.com:8888/get_task","None",'{"result":"fail","err":"unknown"}'))
    masterlogging.debug(LogicLog("asbde1893455","add-task","ok","None"))
    masterlogging.error(SystemLog(utils.get_cur_info(),"bomb","break,bomb"))
    os.system("pause")