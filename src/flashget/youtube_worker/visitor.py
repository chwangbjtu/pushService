import urllib2
from hashlib import md5
import json
import logging
import logging.handlers
import time
import datetime
import os
import signal
import etc

class visitor:

    def get_msg(self):#only used for youku
        cnt = 0
        site=""
        taskid = ""
        vid = ""
        while cnt < etc.retry_num:
            try:
                jjson = {}
                jjson["op"] = etc.op
                jjson["site"] = "youtube"
                reqstr = json.dumps(jjson)
                requrl = "http://" + etc.master_ip +":" + str(etc.master_port) + "/get_task"
                f = urllib2.urlopen(requrl,reqstr)
                res =  f.read()
                logging.info("get msg from flashrouter :" + str(res))
                try:
                    rjson = json.loads(res)
                    ret = rjson["ret"]
                    if ret == "0":
                        taskid = rjson["task_id"]
                        vid = rjson["vid"]
                        site = rjson["site"]
                except Exception, err:
                    logging.error("request task info error:" + str(err))
                    logging.error("master returns:" + str(res))
                break
            except Exception, err:
                logging.error("request task error:" + str(err))
                cnt = cnt + 1
                time.sleep(1)
        return (site,taskid,vid)


    def download_ok(self,task_id,vid):
        sres = "0"
        try:
            trynum = 0
            filename = etc.DATA_PATH + str(vid)
            if not  os.path.exists(filename):
                sres = "1"
                #return "1"
            while trynum < etc.retry_num and os.path.exists(filename):
                res = self.copy_file(vid)
                sres = "0"
                if res != 0:
                    sres = "1"
                else:
                    break
                trynum += 1
        except Exception, err:
            logging.error(str(id) + ":" + str(err))
            sres = "1"
        #if sres == "0":
        self.update_task("youtube",task_id,vid,"0");
        #else:
        #    logging.error("copy_file err,cannot update_task")
        if os.path.exists(filename):
            os.remove(str(filename))

    def copy_file(self,vid):
        info = None
        try:
            vidurl = None
            jsonstr = None
            if id != None:
                import subprocess
                filename = etc.DATA_PATH + vid
                #dest = "crawler@" + str(etc.UGC_IP) + ":" + str(etc.UGC_FILE_PATH)

                #p = subprocess.Popen(["scp","-i","./key/id_rsa", "-P", etc.UGC_PORT, str(filename), str(dest)])
                str1 = "/usr/bin/rsync -avzP --password-file=/youtube_worker/rt/rsync.passwd " + filename + " spider@111.161.35.219::ugc/"
                start = int(time.time())
                p = subprocess.Popen(str1,shell=True)
                while True:
                    res = None
                    res =  p.poll()
                    time.sleep(1)

                    now = int(time.time())
                    if now - start > etc.time_out:
                        os.kill(p.pid, signal.SIGKILL)
                        os.waitpid(-1, os.WNOHANG)
                        return 1

                    if res is None:
                        pass
                    else:
                        p.wait()
                        break
                
                #os.remove(str(filename))
        except Exception, err:
            logging.error(str(vid) + ":" + str(info))
            logging.error(str(err))
            time.sleep(1)
        return 0

    def md5_file(self,name):
        try:
            m = md5()
            a_file = open(name, 'rb')
            m.update(a_file.read())
            a_file.close()
            return m.hexdigest()
        except Exception, err:
            logging.error(str(name) + ":" + str("check md5 error"))
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

                filename = etc.DATA_PATH + vid
                md5str = self.md5_file(filename)
                if not md5str:
                    md5str = ""
                    jjson["ret"] = "1"
                    #return None

                jjson["url"] = etc.DATA_URL + vid + "#md5=" + str(md5str)
                reqstr = json.dumps(jjson)
                f = urllib2.urlopen(requrl,reqstr)
                res =  f.read()
                logging.info("update_task req : " + str(reqstr))
                logging.info("update_task resp : " + str(res))
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
        
