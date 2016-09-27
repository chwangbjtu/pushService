#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import time
import random
import re
import json
import tornado.httpclient as httpclient
import urllib2

import etc
import video_manager

def find_matched_port(ip):
    key_list = {}
    key_list['121.12.101.131'] = '8080'
    key_list['115.238.189.2'] = '80'
    key_list['222.73.131.139'] = '8080'
    key_list['124.232.151.187'] = '8080'
    return "80" if not key_list.has_key(ip) else str(key_list[ip])
    
class MazeHttpResponse():
    def __init__(self, error = 0, code = 200, body = ""):
        self.error = error
        self.code  = code
        self.body  = body
        
class MazeTask():
    def __init__(self, task):
        self._task = task
        self._manager = video_manager.get_video_manager()##
    def _is_short_circuit_task(self, task):
        return (task['uid'] in etc.URGENT_USER) and (task['priority'] == 7) and task['audit_free'] 
    
    def execute(self):
        raise NotImplementedError("execute method is not implemented")

class MazeClientTask(MazeTask):
    def __init__(self, task):
        MazeTask.__init__(self, task)
        #self._http_client  = httpclient.AsyncHTTPClient()
    def _compose_request(self):
        raise NotImplementedError("execute method is not implemented")
        
    def execute(self):
        error = 0
        code  = 200
        body  = ""
        try:
            remote, request = self._compose_request()
            logging.debug("will post request to %s\n%s", remote, request)
            opener = urllib2.build_opener()
            response = opener.open(remote, request, timeout = 30)
            code = response.getcode()
            body = response.read()
        except Exception, err:
            logging.warning("exception when request remote %s %s", remote, err)
            error = 1
        self._handle_response(MazeHttpResponse(error, code, body))
        
    def _handle_response(self, response):
        raise NotImplementedError("execute method is not implemented")

class MazeServerTask(MazeTask):
    def __init__(self, task):
        MazeTask.__init__(self, task)
    def _compose_response(self, result):
        return json.dumps(result)
        
class QueryStatTask(MazeServerTask):
    def __init__(self, task):
        MazeServerTask.__init__(self, task)
        self._result = None
        
    def execute(self):
        try:
            result = self._manager.query_stat_task(self._task)
            return self._compose_response(result)
        except Exception:
            return json.dumps({"result": "fail"})
        finally:
            pass
            
class AuditVideoTask(MazeServerTask):
    def __init__(self, task):
        MazeServerTask.__init__(self, task)
        self._result = None
    
    def _parse_audit_video_task(self):
        self._task['uid'] = int(self._task['uid'])
        if self._task.get('description'):  
            self._task['description'] = self._task['description']
            if self._task['description'] == '':
                self._task['description'] = " "
        else:
            self._task['description'] = " "
 
    def _compose_response(self, result):
        if result['result']:
            result['result'] = 'ok'
        else:
            result['result'] = 'fail'
        return json.dumps(result)
        
    def _is_valid_request(self):
        if self._task['pass']:
            return self._task['uid'] != "" and self._task['title'] != "" and  self._task['tags'] != "" and self._task['channel'] != "" and self._task['description'] != "" and self._task['logo'] != ""  and self._task['ttype'] != ""
        else:
            return self._task['uid'] != ""
        
    def execute(self):
        try:
            if not self._is_valid_request():
                logging.info("invalid request %s", str(self._task)) 
                return json.dumps({"result": "fail"})
                
            self._parse_audit_video_task()
            result = self._manager.audit_video_task(self._task)
            return self._compose_response(result)
        except Exception, err:
            logging.warning("exception when dealing audit task: %s ", str(err))
            return json.dumps({"result": "fail"})
            
class AddVideoTask(MazeServerTask):
    def __init__(self, task):
        MazeServerTask.__init__(self, task)
        self._result = None
    
    def _parse_add_video_task(self):
        self._task['uid'] = int(self._task['uid'])
        if not self._task.get('priority'):
            self._task['priority'] = 1
        else:
            self._task['priority'] = int(self._task['priority'])

        if not self._task.get('pub_time'):
            self._task['pub_time'] = "2013-01-01"

        if self._task.get('describe'):  
            self._task['description'] = self._task['describe']
            if self._task['description'] == '':
                self._task['description'] = " "
        else:
            self._task['description'] = " "

        self._task['step'] = "submit"
        
        if self._is_audit_free(self._task):
            self._task["audit_free"] = 1
        else:
            self._task["audit_free"] = 0 
            
    def _compose_response(self, result):
        if result['result']:
            result['result'] = 'ok'
        else:
            result['result'] = 'fail'
        return json.dumps(result)
        
    def _is_valid_request(self):
        return self._task['uid'] != "" and self._task['title'] != "" and  self._task['tags'] != "" and self._task['channel'] != "" and self._task['origin'] != "" and self._task['site'] != ""
        
    def _is_audit_free(self, task):
        return task['site'] == 'kkn' or (task['site'] == 'cntv' and task['channel'].find(u"\u65B0\u95FB") == 0) or (task.has_key("audit_free") and task['audit_free'] == "yes")
        
    def execute(self):
        try:
            if not self._is_valid_request():
                logging.info("invalid request %s", str(self._task)) 
                return json.dumps({"result": "fail"})
                
            self._parse_add_video_task()
            result = self._manager.add_video_task(self._task)
            return self._compose_response(result)
        except Exception, err:
            logging.warning("exception when dealing add task: %s ", str(err))
            return json.dumps({"result": "fail"})

class TranscodeVideoTask(MazeServerTask):
    def __init__(self, task):
        MazeServerTask.__init__(self, task)

    def _compose_response(self, result):
        response = result
        for task in  response['task_list']:
            if etc.TRANSCODE_FREE:
                task["transcode_free"] = True
            if etc.MASAIC_FREE:
                task["masaic_free"]    = True
            if etc.LOGO_FREE:
                task["logo_free"]      = True
        if response["result"]:
            response["result"] = 'ok'
        else:
            response["result"] = 'fail'
        return json.dumps(response)
    def execute(self):
        try:
            result = self._manager.get_transcode_tasks(self._task)
            return self._compose_response(result)
        except Exception, err:
            logging.warning("exception when dealing requesting transcode task: %s ", str(err))
            return json.dumps({"result": "fail", "err": {"code": "00.00", "info": "can not request transcode task"}})
            
class ReportVideoIdTask(MazeServerTask):
    def __init__(self, task):
        MazeServerTask.__init__(self, task)
        
    def _compose_response(self, result):
        if result['result']:
            result['result'] = 'ok'
        else:
            result['result'] = 'fail'
        return json.dumps(result)
        
    def execute(self):
        try:
            result = self._manager.add_taskid_tid(self._task)
            return self._compose_response(result)
        except Exception, err:
            logging.warning("exception when dealing report cloud id task: %s ", str(err))
            return json.dumps({"result": "fail"})
            
class ReportTranscodeTask(MazeServerTask):
    def __init__(self, task):
        MazeServerTask.__init__(self, task)
        
    def _compose_response(self, result):
        if result['result']:
            result['success'] = True
        else:
            result['success'] = False
        return json.dumps(result)
        
    def _parse_transcode_report(self, task):
        self._task['cloud_id'] = str(self._task['task_id'])
        if not task.has_key("data"):
            return
            
        task["transcode"] = []
        for transcode in task["data"]:
            small_img_str = ""
            large_img_str = ""
            third_image = ""
            logging.debug("parse image in the transcode resport ...")
            for img_item in transcode["img_url"]:
                logging.debug("parse image %s", img_item)
                flag = re.search(".*_\d.jpg", img_item)
                if flag:
                    small_img_str += "%s|" % (img_item)
                    flag2 = re.search(".*_3.jpg", img_item)
                    if flag2:  
                        third_image = img_item
                else:
                    large_img_str = img_item
            transcode["small_image"] = small_img_str
            transcode["large_image"] = large_img_str
            transcode["third_image"] = third_image
            
            #filename, file_size, funshion_id, rate, duration, definition, small_image, logo
            transcode["filename"]    = transcode["filename"]
            transcode["file_size"]   = transcode["size"]
            transcode["funshion_id"] = transcode["funshion_id"]
            transcode["rate"]        = transcode["rate"]
            transcode["duration"]    = transcode["milliseconds"]
            transcode["definition"]  = transcode["definition"]
            # transcode["small_image"] = refer above small_image 
            # transcode["large_image"] = refer above large_image 
            transcode["logo"]        = None
            task["transcode"].append(transcode)
        logging.debug("%d transcode files in the transcode report", len(task["transcode"]))
        
    def  _is_transcode_task_ok(self):
        return self._task.get('task_id') #and self._task.get('result') and self._task.get('data')    
    
    def execute(self):
        try:
            if self._is_transcode_task_ok():
                self._parse_transcode_report(self._task)
            else:
                logging.info("invalid transcode report %s ", str(self._task))
                self._task["result"] = False# let this is failed task
                
            result = self._manager.add_transcode_report(self._task)
            return self._compose_response(result)
        except Exception, err:
            logging.warning("exception when dealing report transcode result: %s ", str(err))
            return json.dumps({"success": False})
        
class NotifyPackageTask(MazeClientTask):
    def __init__(self, task):
        MazeClientTask.__init__(self, task)
   
    def _compose_request(self):
        request = {}
        remote = etc.CLOUD_SERVICE_IP + ":" + str(etc.CLOUD_SERVICE_PORT) + etc.cloud_notify_pack_dat
        request["task_id"] = [self._task["cloud_id"]]
        
        request['pack_result_notify'] = "http://%s:%s%s" % (etc.MAZE_IP, etc.SERVICE_PORT, etc.cloud_notify_loaded_info)
        remote = "http://" + remote 
        return [remote, json.dumps(request)]
        
    def _handle_response(self, response):
        if response.error or response.code != 200:
            logging.info("failed to submit task [cloud-id %s, tid %s] for packaging, will re-submit package", self._task["cloud_id"], self._task["tid"])
            return
        if not self._manager.set_package_start(self._task):
            logging.info("failed to update task [cloud-id %s, tid %s] status in db, will re-submit package", self._task["cloud_id"], self._task["tid"])
            return
        logging.debug("task [cloud-id %s, tid %s] has been submitted to cloud for packaging", self._task["cloud_id"], self._task["tid"])    
        
class ReportPackageTask(MazeServerTask):
    def __init__(self, task):
        MazeServerTask.__init__(self, task)

    def _compose_response(self, result):
        if result['result']:
            result['success'] = True
        else:
            result['success'] = False
        return json.dumps(result)
        
    def _parse_package_report(self):
        if self._task.has_key("result") and self._task["result"] == True:
            self._task["ip"]   = self._task["server_ip"]
            self._task["server_port"] = find_matched_port(self._task["ip"])
            self._task["port"] = self._task["server_port"]
        
    def execute(self):
        try:
            self._parse_package_report()
            result = self._manager.add_package_report(self._task)
            return self._compose_response(result)
        except Exception, err:
            logging.warning("exception when dealing report package result %s %s ", json.dumps(self._task), str(err))
            return json.dumps({"success": False})
           
class NotifyDistributeTask(MazeClientTask):
    def __init__(self, task):
        MazeClientTask.__init__(self, task)
        self._task = task
        
    def _compose_transcode(self, transcode):
        #filename, file_size, funshion_id, rate, duration, definition
        video_json = {}
        video_json['filename']      = transcode["funshion_id"]
        video_json['filesize']      = transcode["file_size"]
        video_json['fileformat']    = "mp4"
        video_json['file']          = transcode['filename']
        video_json['rate']          = str(transcode["rate"])
        video_json['definition']    = transcode["definition"]
        video_json['video_length']  = transcode["duration"]

        str_logo                    = transcode["logo"]
        img_rec = transcode["small_image"]

        image_small = img_rec.split("|")
        if len(image_small) < 3:
            image_small = ""
        else:
            image_small = image_small[2]
            image_small = image_small.rstrip()
            if re.match(".*_0.jpg", image_small):
                image_small = image_small.replace('0.jpg', '2.jpg')

        return [video_json, str_logo, image_small]
        
    def _compose_video(self, video):
        username = self._manager.get_auth_user(video['uid'])
        if not username:
            return None
        videos_json = {}
        videos_json['title']                = video['title']
        videos_json['tags']                 = video['tags']
        videos_json['first_guide']          = video['channel']
        videos_json['description']          = video['description']
        videos_json['owner']                = username # to-do remember to update it when loaded from db or add new video
        videos_json['owner_upload_time']    = str(time.time())
        videos_json['total_views']          = str(random.randint(0, 100))
        videos_json['forwards']             = "0"
        videos_json['comments']             = str(random.randint(0, 100))
        videos_json['img_path']             = "image_small"
        site = video['site']
        videos_json['source'] = "kankan" if (site == 'kkn' or site == 'cntv') else "ugc"
        videos_json['guide_type'] = 1 if (site == 'brave') else 0
        img_list = []
        videos_json['img_path'] = None
        videos_json['video'] = []
        for transcode in video["transcode"]:
            try:
                trans_file, logo, img = self._compose_transcode(transcode)
                if trans_file:
                    videos_json['video'].append(trans_file)
                if logo:
                    videos_json['img_path'] = logo
                if img:
                    img_list.append(img)
            except Exception, err:
                logging.warning("exception when composing transcode file %s", err)
                continue
        if not videos_json['img_path'] and len(img_list) > 0:
            videos_json['img_path'] = img_list[random.randint(0, len(img_list) - 1)]
        return videos_json
        
    def _compose_request(self):
        videos_list = {}
        videos_list['ih']       = self._task['infohash']
        videos_list['size']     = self._task['size']
        videos_list['dat_name'] = self._task['infohash']
        videos_list['ip']       = self._task['ip']
        videos_list['port']     = self._task['port']
        videos_list['videos']   = []
        for tid in self._task["tid"]:
            video = self._task["tid"][tid]
            try:
                final_video = self._compose_video(video)
                if final_video:
                    videos_list['videos'].append(final_video)
                else:
                    logging.info("invalid video %s, ignore it", tid)
            except Exception, err:
                logging.warning("exception when composing video %s %s", tid, err)
                continue
        data = json.dumps(videos_list)
        request = {}
        request['data'] = data
        logging.debug("distribute the task \n%s", json.dumps(request))
        import urllib
        request = urllib.urlencode(request)
        remote = "http://" + etc.macros_ip + etc.macros_method

        return [remote, request]
        
    def _handle_response(self, response):
        if response.error:
            logging.info("failed to submit task distribute task due to error, will re-submit the task %s", self._task["infohash"])
            return
        if response.code != 200 or response.body != "return=ok":
            logging.info("failed to submit task distribute task due to macross, will re-submit the task %s", self._task["infohash"])
            return
        if not self._manager.set_distribute_start(self._task):
            logging.info("failed to update distribute task %s status in db, will re-submit it", self._task["infohash"])
            return
        logging.debug("distribute task %s has been submitted", self._task["infohash"])     
