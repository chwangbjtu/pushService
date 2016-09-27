#!/usr/bin/python
# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import json
from threading import Thread
import logging

import etc
import error
from maze_task import *

class HttpServer(Thread):
    _HTTP_RESP1 = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:"
    def __init__(self, port):
        Thread.__init__(self)
        self._port = port
        #self._http_business   = http_business.HttpBusiness()
        #self._web_business    = web_business.HttpBusiness()
        #self._cloud_business  = cloud_business.CloudBusiness()
        self.__command_handlers = {}
        self.__command_handlers[etc._URL_MAZE_POST_TASK]        = self.handle_add_video
        self.__command_handlers[etc._URL_MAZE_POST_AUDIT]       = self.handle_audit_video
        self.__command_handlers[etc.cloud_get_tasklist]         = self.handle_request_task
        self.__command_handlers[etc.cloud_add_taskmap]          = self.handle_add_taskid_tid_map
        self.__command_handlers[etc.cloud_transcode_report]     = self.handle_report_transcode_video
        self.__command_handlers[etc.cloud_notify_loaded_info]   = self.handle_report_package_video
        
        # self.__command_handlers[etc._ADD_TASK_STATUS]           = self.handle_add_task_status
        # self.__command_handlers[etc._GET_TASK_STATUS]           = self.handle_get_task_status
        # self.__command_handlers[etc._ADD_VIDEO_URL]             = self.handle_add_video_url
        # self.__command_handlers[etc._MAZE_QUERY_INFO]           = self.handle_query_maze_info
        # self.__command_handlers[etc._MAZE_2MACROS_INFO]         = self.handle_query_macros_info
        self.__command_handlers["/mgmt/logging"]                = self.handle_logging_level
        self.__command_handlers["/mgmt/stat"]                   = self.handle_stat
        
        #self._http_mgmt = http_mgmt.HttpMgmt()
        #self.__analytics = tm_analytics.Analytics.instance()
       
        self.__logger = logging.getLogger()
        
    def handle_stat(self, request):
        try:
            logging.debug("handle request from %s with body %s", request.remote_ip, request.body)
            return QueryStatTask(None).execute()
        except Exception, err:
            logging.warning("exception when handling web post request: %s", str(err))
            return "{\"result\":\"fail\"}"
            
    def handle_logging_level(self, request):
        _loglevel = {'DEBUG': logging.DEBUG, 'INFO':logging.INFO, \
                     'WARNING':logging.WARNING, 'ERROR':logging.ERROR, 'CRITICAL':logging.CRITICAL}
                
        level = ""
        if request.arguments.has_key("level"):
            level = request.arguments["level"][0]
        
        if level != "" and (_loglevel.has_key(level)):
            self.__logger.setLevel(_loglevel[level])
            _debug = "The logger level is set to %s" % (level)
            self.__logger.debug( _debug )
            return _debug
        else:
            _info = "can not set log level %s" % (level)
            self.__logger.info( _info )
            return "wrong level: %s" % (level)

    # def handle_query_maze_info(self, request):
        # return self._http_mgmt.query_num()

    # def handle_query_macros_info(self, request):
        # query_time = request.arguments["time"][0]
        # print query_time
        # return self._http_mgmt.query_dat_sort(query_time)

    '''
     流程环节状态上报信息入库
    '''
    # def handle_add_task_status(self, request):
        # try:
            # task_body = json.loads(request.body)
            # tid = None
            # step = None
            # status = None
            # try:
                # flag = 0
                # tid = task_body["tid"]
                # step = task_body["step"]
                # status = task_body["status"]
            # except Exception, e:
                # logging.warning("exception when add task status: %s", str(e))
                # return error.pack_errinfo_json(error.STATUS_ADD_ERROR)
            # if tid == None or step == None or status == None:
                # logging.info("wrong json format: %s", task_body)
                # return error.pack_errinfo_json(error.STATUS_ADD_ERROR)
            # res_flag = self._http_business.add_taskstatus2(tid, step, status)
            # if res_flag == constant.FAIL:
                # logging.info("failed to add task status (%s)", task_body)
                # return error.pack_errinfo_json(error.STATUS_ADD_ERROR)
            # elif res_flag == constant.FORBIDDEN:
                # logging.info("add task status is forbiddened (%s)", task_body)
                # return error.pack_errinfo_json(error.STATUS_ADD_FORBIDDEN)
            # logging.debug("add task status tid %s, step %s, status %s", tid, step, status)
            # return "{\"result\":\"ok\"}"
        # except Exception, e:
            # logging.warning("exception when adding task status: %s", str(e))
            # return error.pack_errinfo_json(error.ERROR_PARAM_URL)

    # def handle_add_video_url(self, request):
        # try:
            # task_body = json.loads(request.body)
            # tid = task_body["tid"]
            # url = task_body["url"]
            # res_flag = self._http_business.add_taskvideourl(tid, url)
            # if res_flag == constant.FAIL:
                # logging.info("failed to add video url %s", task_body)
                # return error.pack_errinfo_json(error.STATUS_ADD_ERROR)
            # elif res_flag == constant.FORBIDDEN:
                # logging.info("add video url is forbiddened (%s)", task_body)
                # return error.pack_errinfo_json(error.STATUS_ADD_FORBIDDEN)
        # except Exception, e:
            # logging.warning("exception when adding video url: %s", str(e))
            # return error.pack_errinfo_json(error.ERROR_PARAM_URL)
        # else:
            # logging.debug("add video url with tid %s, url %s", tid, url)
            # return "{\"result\":\"ok\"}"

    # def handle_get_task_status(self, request):
        # value_list = []
        # try:
            # task_id = request.arguments["tid"][0]
            # value_list = self._http_business.get_taskstatus(task_id)
            # if (len(value_list) == 0):
                # return "[]"
            # resp = json.dumps(value_list)
            # logging.debug("get task %s status: %s ", task_id, resp)
            # return resp
        # except Exception, e:
            # logging.warning("exception when getting task status: %s", str(e))
            # return "[]"
    def handle_audit_video(self, request):
        try:
            logging.debug("handle request from %s with body %s", request.remote_ip, request.body)
            if request.method != "POST":
                logging.info("this is not POST method: %s", request.method)
                body = error.pack_errinfo_json(error.ERROR_HTTP_METHOD_NOT_SUPPORTED)
                return body
            return AuditVideoTask(json.loads(request.body)).execute()
        except Exception, err:
            logging.warning("exception when handling web post request: %s", str(err))
            return "{\"result\":\"fail\"}"

    #spider或forward申请任务内容入库
    def handle_add_video(self, request):
        try:
            logging.debug("handle request from %s with body %s", request.remote_ip, request.body)
            if request.method != "POST":
                logging.info("this is not POST method: %s", request.method)
                body = error.pack_errinfo_json(error.ERROR_HTTP_METHOD_NOT_SUPPORTED)
                return body
            return AddVideoTask(json.loads(request.body)).execute()
        except Exception, err:
            logging.warning("exception when handling web post request: %s", str(err))
            return "{\"result\":\"fail\"}"


    #task_mgr 从maze获取任务列表
    def handle_request_task(self, request):
        try:
            req = {}
            task_num = int(request.arguments["num"][0])
            req["num"] = task_num
            return TranscodeVideoTask(req).execute()
        except Exception, err:
            logging.warning("exception when handling get task list request: %s", str(err))
            return json.dumps({"result":"fail", "err": {"code": "00.00", "info": "can not request transcode task"}})
            
    
    #保存云转码服务任务标识task_id与ugc内部tid对应关系
    def handle_add_taskid_tid_map(self, request):
        try:
            if request.method != "POST":
                logging.info("this is not POST method: %s", request.method)
                body = error.pack_errinfo_json(error.ERROR_HTTP_METHOD_NOT_SUPPORTED)
                return body
            return ReportVideoIdTask(json.loads(request.body)).execute()
        except Exception, err:
            logging.warning("exception when handling add task map: %s", str(err))
            return "{\"result\":\"fail\"}"

    
    # 云转码上报转码信息入库
    def handle_report_transcode_video(self, request):
        try:
            task_body = request.body
            if task_body == "":
                logging.info("invalid request with empty body")
                return "parameter error."#重大疑问，这时候返回“parameter error”外层有对这个字符串进行判断吗？，这时候返回该MS的具体消息是什么？
            return ReportTranscodeTask(json.loads(request.body)).execute()#疑问，是否需要像原代码一样判断是否执行成功，个人认为不需要，应该直接返回失败
        except Exception, err:
            logging.warning("exception when handling transcode report: %s", str(err))
            return "{\"result\":\"fail\"}"
        
    '''
    云转码上报打包加载信息入库
    '''
    def handle_report_package_video(self, request):
        try:
            return ReportPackageTask(json.loads(request.body)).execute()
        except Exception, err:
            logging.warning("exception when handling loaded ms info: %s", str(err))
            return "{\"result\":\"fail\"}"
        
    def handle_apply_task(self, request):
        request = request
        try:
            pass
        except Exception:
            pass
    
    def handle_request(self, request):
        logging.debug("receive request for %s: \n%s", request.uri, request.body)
        if request.uri not in self.__command_handlers and request.method == "POST":
            body = error.pack_errinfo_json(error.ERROR_HTTP_URL_NOT_SUPPORTED)
        elif (not self.__command_handlers.has_key(request.path.lower())) and request.method == "GET":
            body = error.pack_errinfo_json(error.ERROR_HTTP_URL_NOT_SUPPORTED)
        else:
            url = None
            if request.method == "POST":
                url = request.uri
            else:
                url = request.path.lower()
            #ip = request.remote_ip
            handler = self.__command_handlers[url]
            body = handler(request)

        message = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:%d\r\n\r\n%s" % (
                                                                  len(body), body)
        logging.debug("reply with: %s", body)
        request.write(message)
        request.finish()
    
    def run(self):
        logging.critical( "thread [%s] starts to run ... ", self.getName() )
        logging.info("start http server with port = %s", self._port)
        http_server = tornado.httpserver.HTTPServer(self.handle_request, no_keep_alive = True)
        http_server.listen(int(self._port))
        tornado.ioloop.IOLoop.instance().start()

def __test2():
    body = "123123123"
    message = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:%d\r\n\r\n%s" % (len(body), body)
    #print message

if __name__ == "__main__":
    __test2()

