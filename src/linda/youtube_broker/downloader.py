#-*- coding: utf-8 -*-
import threading
import logging
import json  
import time
import traceback
import os
import etc
from common import http_download
from common import idmgr
from common import util


class Cdownloader(threading.Thread):
    def __init__(self):  
        threading.Thread.__init__(self)  
        self.gettaskurl = "http://" + str(etc.master_domain) + "/get_task?" + "broker_port=" + str(etc.service_port) + "&broker_type=agent"
        self.reporturl = "http://" + str(etc.master_domain) + "/report_download_result"
        self.httpdownloader = http_download.HTTPDownload()
        self.idmgr = idmgr.Idmgr.instance()
        self.util = util.Util()
   
    def run(self):
        while True:
            id = ""
            durl = ""
            dst_path = ""
            success = "failed"
            try:
                #拉取任务
                (id,durl,dst_path) = self.get_task()
                logging.debug("get task over :%s,%s,%s" % (str(id),str(durl),str(dst_path)))
                if id:
                    logging.debug("get task over :%s,%s,%s" % (id,durl,dst_path))
                    self.idmgr.set_id(id)
                    dres = self.gdownload(id,durl,dst_path)
                    ext = ""
                    size = ""
                    if dres:
                        (ext,size,file_path_name) = self.get_file_info(id,dst_path)
                        rres = self.gsync_file(id,dst_path,ext)
                        if rres:
                            success = "success"

                    self.report_task(id,success,"",ext,size)
                    self.clear_file() 
            except Exception, e:
                logging.error(traceback.format_exc())
            finally:
                self.idmgr.clear_id()

            if success != "success":
                time.sleep(etc.pull_task_interval) 

    def clear_file(self):
        try:
            self.util.del_data_dir(etc.download_path)
        except Exception, e:
            logging.error(traceback.format_exc())

    def get_task(self):
        try:
            data = self.httpdownloader.get_data(self.gettaskurl)
            loginfo = "request : %s,response : %s" % (str(self.gettaskurl),str(data))
            logging.info(loginfo)
            if data:
                jdata = json.loads(data)
                result = jdata.get("result",None)
                if result == "success":
                    id = jdata.get("id",None)
                    durl = jdata.get("url",None)
                    dst_path = jdata.get("dst_path",None)
                    if id and durl and dst_path:
                        return (id,durl,dst_path)
        except Exception, e:
            logging.error(traceback.format_exc())
        return (None,None,None)

    def report_task(self,id,result,msg,ext,size):
        res = False
        try:
            while True:
                jinfo = {}
                jinfo["id"] = str(id)
                jinfo["result"] = str(result)
                jinfo["msg"] = str(msg)
                jinfo["ext"] = str(ext)
                jinfo["size"] = str(size)
                jinfo["broker_port"] = str(etc.service_port)
                info = json.dumps(jinfo)

                data = self.httpdownloader.post_data(self.reporturl,info)
                loginfo = "report_download_result: url is: %s,body is:%s ,resp is:%s" % (self.reporturl,info,str(data))
                logging.info(loginfo)
                if not data:
                    time.sleep(etc.report_task_interval)
                    continue
                else:
                    res = True
                    break
        except Exception, e:
            logging.error(traceback.format_exc())

        return res

    def gsync_file(self,id,dst_path,ext):
        res = False
        try:
            i = 0
            while i < etc.resync_num:
                res = self.sync_file(id,dst_path,ext)
                if not res:
                    i = i + 1
                    time.sleep(1)
                    continue
                else:
                    break
        except Exception, e:
            logging.error(traceback.format_exc())

        return res

    def sync_file(self,id,dst_path,ext):
        res = False
        try:
            import subprocess
            filename = etc.download_path + str(id) +"." + str(ext)
            #/usr/bin/rsync -avzP --password-file=/youtube_worker/rt/rsync.passwd /tmp/rt.tar.gz  rsync://root@59.172.252.67:22221/ugc/media/linda/20150909/m23821/m1000.mp4
            #str1 = "/usr/bin/rsync -avzP --password-file=/youtube_worker/rt/rsync.passwd " + filename + " spider@111.161.35.219::ugc/"
            #str1 = "/usr/bin/rsync -avzP --password-file=" + etc.sync_master_password_file + " " + filename + " " + etc.sync_master_info +str(dst_path) + "." +str(ext)
            #"/usr/bin/rsync -avzP --password-file=/tmp/rsync.passwd  tmp_dir/  rsync://root@172.17.20.91:873/ugc/"
            str1 = "/usr/bin/rsync -avzP --password-file=" + etc.sync_master_password_file + " " + etc.download_path + " " + etc.sync_master_info
            logging.debug(str1)
            #return True
            start = int(time.time())
            p = subprocess.Popen(str1,shell=True)
            while True:
                res = None
                res =  p.poll()
                time.sleep(1)

                now = int(time.time())
                if now - start > etc.sync_timeout:
                    os.kill(p.pid, signal.SIGKILL)
                    os.waitpid(-1, os.WNOHANG)
                    return res

                if res is None:
                    pass
                else:
                    p.wait()
                    res = True
                    break
        except Exception, e:
            logging.error(traceback.format_exc())
        return res

    def gdownload(self,id,url,dst_path):
        res = False
        ext = None
        size = None
        filename = ""
        try:
            i = 0
            while i < etc.redownload_num:
                res = self.download(id,url,dst_path)
                logging.debug("downdload res:"+str(res))
                (ext,size,file_path_name) = self.get_file_info(id,dst_path)
                #filename = etc.download_path+str(id) + "." + str(ext)
                filename = file_path_name
                logging.debug("filename:"+filename)
                if not res or not os.path.exists(filename):
                    logging.debug("info:"+str(res)+";file exits "+str(os.path.exists(filename)) +",filename:" + filename)
                    i = i + 1
                    time.sleep(1)
                    continue
                else:
                    break
            if not os.path.exists(filename):
                res = False
        except Exception, e:
            logging.error(traceback.format_exc())
        return res

    def download(self,id,url,dst_path):
        res = False
        try:
            if url == None or len(url) == 0:
                return res

            import subprocess
            #ext 显示文件后缀,视频类型，mp4,flv;--no-playlist 不下载列表，只下载列表中的一个:q
            
            filepath = self.util.get_download_file_path(etc.download_path,dst_path)
            if not self.util.create_data_dir(etc.download_path,dst_path):
                logging.error("create_data_dir error ,dst_path:" + dst_path)
                return res
            filename = filepath + id + ".%(ext)s"
            p = subprocess.Popen(["./youtube-dl","--no-playlist","-o",filename,url])
            while True:
                tres = None
                tres =  p.poll()
                if tres != None:
                    time.sleep(1)
                else:
                    p.wait()
                    res = True
                    break
        except Exception, e:
            logging.error(traceback.format_exc())
        return res

    def get_file_info(self,id,dest_path):
        file_path_name = None
        ext = None
        size = None
        try:
            #file_path = etc.download_path+id
            file_path = self.util.get_download_file_path(etc.download_path,dest_path)
            file_list = self.util.search_file(id,file_path)
            if file_list:
                for item in file_list:
                    file_path_name = file_path+file_list[0]
                    ext = self.util.get_file_ext(file_path_name)
                    if ext == "part":
                        continue
                    size = self.util.get_file_size(file_path_name)
        except Exception, e:
            logging.error(traceback.format_exc())
        return (ext,size,file_path_name)


if __name__ == "__main__":
    cd = Cdownloader()
    cd.start()
