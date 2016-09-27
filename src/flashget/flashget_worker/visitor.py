import urllib2
from hashlib import md5
import json
import logging
import logging.handlers
import time
import etc

class visitor:

    def get_msg(self):#only used for youku
        cnt = 0
        site=None
        taskid = None
        vid = None
        src_url = None
        while cnt < etc.retry_num:
            try:
                jjson = {}
                jjson["op"] = etc.op
                reqstr = json.dumps(jjson)
                requrl = "http://" + etc.master_ip +":" + str(etc.master_port) + "/get_task"
                f = urllib2.urlopen(requrl,reqstr)
                res =  f.read()
                try:
                    rjson = json.loads(res)
                    ret = rjson["ret"]
                    logging.info("get_task:" + str(res))
                    if ret == "0":
                        taskid = rjson["task_id"]
                        vid = rjson["vid"]
                        site = rjson["site"]
                        src_url = rjson["src_url"]
                except Exception, err:
                    logging.error("request task info error:" + str(err))
                    logging.error("master returns:" + str(res))
                break
            except Exception, err:
                logging.error("request task error:" + str(err))
                cnt = cnt + 1
                time.sleep(1)
        return (taskid,site,vid,src_url)

    def md5_file(self,taskid,name):
        try:
            m = md5()
            a_file = open(name, 'rb')
            m.update(a_file.read())
            a_file.close()
            return m.hexdigest()
        except Exception, err:
            logging.error(taskid + ":" + str(name) + ":" + str("check md5 error"))
            logging.error(str(err))
        return None

    def update_task(self,site,task_id,vid,ret):
        cnt = 0
        #while cnt < etc.retry_num:
        while True:
            try:
                requrl = "http://" + etc.master_ip +":" + str(etc.master_port) + "/update_task"
                jjson = {}
                jjson["site"] = site
                jjson["task_id"] = task_id
                jjson["ret"] = ret

                filename = etc.data_path + vid
                md5str = self.md5_file(task_id,filename)
                if not md5str  and int(ret) == 0:
                    md5str = ""
                    jjson["ret"] = "1"
                    #return None
                if int(ret) != 0:
                    md5str = ""

                jjson["url"] = etc.url_path + vid + "#md5=" + str(md5str)
                reqstr = json.dumps(jjson)
                f = urllib2.urlopen(requrl,reqstr)
                res =  f.read()
                #print res
                try:
                    rjson = json.loads(res)
                    ret = rjson["ret"]
                    logging.info("update_task site " + site +" task_id " + task_id + " ret " + ret)
                    break
                except Exception, err:
                    logging.error("update task info error:" + str(err))
                    logging.error("master returns:" + str(res))
                    break
            except Exception, err:
                logging.error("update task error:" + str(err))
                cnt = cnt + 1
                time.sleep(1)
        
        #return (site,id)
