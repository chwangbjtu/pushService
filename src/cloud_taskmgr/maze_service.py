#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import tornado.httpclient
import error
import config_loader
import logging

#asynchronize
def require_task(count,cb_func):
    maze_ip,maze_port = config_loader.get_maze_addr()
    url = "http://%s:%s/maze/get_tasklist?num=%d" % (maze_ip,maze_port,count)
    request = tornado.httpclient.HTTPRequest(url,method="GET",request_timeout=20,connect_timeout=20)
    http_client = tornado.httpclient.AsyncHTTPClient()
    try:
        handler = RequireTaskHandler(cb_func)
        http_client.fetch(request,handler.handle)
    except tornado.httpclient.HTTPError,e:
        logging.warning("exception when requesting task from maze: %s", str(e))
        return (False,error.ERROR_HTTP_REQUEST_INVALID)
    return (True,None)

class RequireTaskHandler(object):
    def __init__(self,next_cb):
        self.__next_cb = next_cb
    def handle(self,response):
        next_cb = self.__next_cb
        if response.error:
            logging.warning("response error when requesting task from maze: %s", str(response.error))
            next_cb(False,error.ERROR_HTTP_REQUEST_TIMEOUT)
            return
        try:
            logging.debug("the message received from maze\n%s", response.body)
            res = json.loads(response.body)
            if res["result"] != "ok":
                err_info = res["err"]["info"]
                err_code = res["err"]["code"]
                logging.info("the request failed due to %s", err_info)
                next_cb(False,(err_info,err_code))
                return
            else:
                logging.debug("to parse task list received from maze")
                task_list = res["task_list"]
                next_cb(True,task_list)
                return
        except Exception,e:
            logging.warning("exception when processing task list response from maze %s", str(e))
            next_cb(False,(error.ERROR_INTERNAL_UNKNOWN_ERROR[0],"%s"%str(e)))


def report_cloud_id(tid,cloud_id,cb_func):
    maze_ip,maze_port = config_loader.get_maze_addr()
    url = "http://%s:%s/maze/report_cloud_id" % (maze_ip, maze_port)
    report_info = {"cloud_id":cloud_id,"tid":tid}
    report_info = json.dumps(report_info)
    request = tornado.httpclient.HTTPRequest(url,method="POST",body=report_info,request_timeout=20,connect_timeout=20)
    http_client = tornado.httpclient.AsyncHTTPClient()
    try:
        logging.debug("report cloud id %s to maze by requesting url %s", cloud_id, url)
        handler = ReportCloudIDHandler(cb_func)
        http_client.fetch(request,handler.handle)
    except tornado.httpclient.HTTPError,e:
        logging.warning("exception when reporting cloud id %s to maze %s", cloud_id, str(e))
        return (False,error.ERROR_HTTP_REQUEST_INVALID)
    return (True,None)

class ReportCloudIDHandler(object):
    def __init__(self,next_cb):
        self.__next_cb = next_cb
    def handle(self,response):
        next_cb = self.__next_cb
        if response.error:
            logging.info("response error when reporint cloud id to maze: %s", str(response.error))
            next_cb(False,error.ERROR_HTTP_REQUEST_TIMEOUT)
            return
        try:
            logging.debug("the message received from maze\n%s", response.body) 
            res = json.loads(response.body)
            if res["result"] != "ok":
                logging.info(("the request failed due to %s", res["err"]["info"]))
                next_cb(False,(res["err"]["code"],res["err"]["info"]))
                return
            else:
                logging.info("response from maze: reporting successfully")
                next_cb(True,None)
                return
        except Exception,e:
            logging.warning("exception when parsing report-cloud-id reponse %s", str(e))
            next_cb(False,error.ERROR_PARAM_ARG_MISSING)