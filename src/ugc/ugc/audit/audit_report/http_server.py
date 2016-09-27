#!/usr/bin/python
# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import json
#import http_mgmt
import http_business
import log
import etc
#import tm_analytics
import error
import constant


class HttpServer:        
    #_ADD_TASK_STATUS = "/ems/addtaskstatus"
    #_GET_TASK_STATUS = "/ems/gettaskstatus"
    #_ADD_VIDEO_URL = "/ems/upload_url"
    _HTTP_RESP1 = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:"
    def __init__(self):       
        #self._http_mgmt = http_mgmt.HttpMgmt()
        self._http_business = http_business.HttpBusiness()
        self.__command_handlers = {}
        #self.__command_handlers[self._ADD_TASK_STATUS] = self.handle_add_task_status
        self.__command_handlers[etc.verify_report] = self.handle_verify_report
        self.__command_handlers[etc.verify_hash] = self.handle_verify_hash
        #self.__command_handlers[etc.verify_exam] = self.handle_verify_exam
        self.__command_handlers[etc.verify_hash_dat] = self.handle_verify_hash_dat
        self.__error_log = log.MakeLog(etc.error_for_process)
        self.__process_log = log.MakeLog(etc.log_for_process)
        self.__process_log.start()
        self.__error_log.start()
        #self.__analytics = tm_analytics.Analytics.instance()
    
    #audit report verify    
    def handle_verify_report(self, request):
        try:
            task_body = request.body
            print "recv verify report: ", task_body
            res_flag = self._http_business.add_transcode_info(task_body)
            if res_flag == constant.FAIL:
                self.__error_log.loginfo("handle_verify_report return error: %s" % (task_body))
                return error.pack_errinfo_json(error.STATUS_ADD_ERROR)
            elif res_flag == constant.FORBIDDEN:
                self.__error_log.loginfo("handle_verify_report forbidden with : %s" % (task_body))              
                return error.pack_errinfo_json(error.STATUS_ADD_FORBIDDEN)
        except Exception, e:
            self.__error_log.loginfo("add_task_status has exception error: %s" % (str(e)))
            return error.pack_errinfo_json(error.ERROR_PARAM_URL)
        else:
            return "{\"result\":\"ok\"}"

    #audit handle_verify_hash   
    def handle_verify_hash(self, request):
        try:
            task_body = request.body
            print "recv verify report: ", task_body
            res_flag = self._http_business.add_package_info(task_body)
            if res_flag == constant.FAIL:
                self.__error_log.loginfo("handle_verify_hash return error: %s" % (task_body))
                return error.pack_errinfo_json(error.STATUS_ADD_ERROR)
            elif res_flag == constant.FORBIDDEN:
                self.__error_log.loginfo("handle_verify_hash forbidden with : %s" % (task_body))
                return error.pack_errinfo_json(error.STATUS_ADD_FORBIDDEN)
        except Exception, e:
            self.__error_log.loginfo("handle_verify_hash has exception error: %s" % (str(e)))
            return error.pack_errinfo_json(error.ERROR_PARAM_URL)
        else:
            return "{\"result\":\"ok\"}"

    def handle_verify_hash_dat(self, request):
        """audit handle last crane report. Record the dat file loaded by mediaserver and mediaserver's addr"""
        try:
            task_body = request.body
            print 'recv ms addr info report:', task_body
            res_flag = self._http_business.add_video_loaded_info(task_body)
            if res_flag == constant.FAIL:
                self.__error_log.loginfo("handle_verify_hash_dat return error: %s" % (task_body))
                return error.pack_errinfo_json(error.STATUS_ADD_ERROR)
            elif res_flag == constant.FORBIDDEN:
                self.__error_log.loginfo("handle_verify_hash_dat forbidden with : %s" % (task_body))
                return error.pack_errinfo_json(error.STATUS_ADD_FORBIDDEN)
        except Exception, e:
            self.__error_log.loginfo("handle_verify_hash_dat has exception error: %s" % (str(e)))
            return error.pack_errinfo_json(error.ERROR_PARAM_URL)
        else:
            return "{\"result\":\"ok\"}"

    def handle_request(self, request):
        if request.uri not in self.__command_handlers:
            body = error.pack_errinfo_json(error.ERROR_HTTP_URL_NOT_SUPPORTED)
        else:
            url = request.uri
            handler = self.__command_handlers[url]
            body = handler(request)
        
        message = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:%d\r\n\r\n%s" % (
                                                                  len(body), body)
        print message
        request.write(message)
        request.finish()

    def start(self, port):
        http_server = tornado.httpserver.HTTPServer(self.handle_request, no_keep_alive = True)
        http_server.listen(int(port))
        tornado.ioloop.IOLoop.instance().start()
        return True

def __test():
    taskserver = HttpServer()
    taskserver.start(6801)

def __test2():
    body = "123123123"
    message = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:%d\r\n\r\n%s" % (len(body), body)
    print message

if __name__ == "__main__":
    __test()



