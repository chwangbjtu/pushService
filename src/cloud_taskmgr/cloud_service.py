#!/usr/bin/python
# -*- coding:utf-8 -*-
import tornado.httpclient
import json
import config_loader
import logging
import error

def post_task2(task, cb_func):
    #cloud url for add task
    cloud_ip,cloud_port = config_loader.get_cloud_addr()
    cloud_url = "http://%s:%s/add_task/" % (cloud_ip,cloud_port)
    #maze url for report transcode info
    maze_ip,maze_port = config_loader.get_maze_addr()
    maze_url = "http://%s:%s/maze/cloud_transcode_report" % (maze_ip,maze_port)
    #pack video parser argument
    source_url = {"site":task["site"], "vid":task["vid"]}
    #add parse para to source_url
    if task['origin'] == 'spider':
        source_url['parse'] = '0'
    elif task['origin'] == 'forwards':
        #uid is 1 from spider
        if int(task['uid']) == 1:
            source_url['parse'] = '0'
        #from ugc
        else:
            source_url['parse'] = '1'
    elif task['origin'] == 'push':
        if task['site'] == 'kkn':
            source_url['parse'] = '1'
        else:
            source_url['parse'] = '0'
    else:
        source_url['parse'] = '0'
    source_url = json.dumps(source_url)
    task_info = task
    task_info["task_type"]  = 1
    task_info["notify_url"] = maze_url
    task_info["source_url"] = source_url
    task_info = json.dumps(task_info)
    #send request
    try:
        logging.debug("post message to cloud service by requesting url %s: %s", cloud_url, task_info)
        request = tornado.httpclient.HTTPRequest(url=cloud_url,method="POST",body=task_info,request_timeout=20,connect_timeout=20)
        http_client = tornado.httpclient.AsyncHTTPClient()
        handler = PostTaskHandler(cb_func)
        http_client.fetch(request,handler.handle)
        return (True,None)
    except Exception,e:
        logging.warning("exception when sending request message to cloud service %s", str(e))
        return (False,error.ERROR_HTTP_REQUEST_INVALID)
        
def post_task(vid,site,priority,cb_func):
    #cloud url for add task
    cloud_ip,cloud_port = config_loader.get_cloud_addr()
    cloud_url = "http://%s:%s/add_task/" % (cloud_ip,cloud_port)
    #maze url for report transcode info
    maze_ip,maze_port = config_loader.get_maze_addr()
    maze_url = "http://%s:%s/maze/cloud_transcode_report" % (maze_ip,maze_port)
    #pack video parser argument
    source_url = {"site":site,"vid":vid}
    source_url = json.dumps(source_url)
    task_info = {"task_type":1,"notify_url":maze_url,"priority":priority,"source_url":source_url}
    task_info = json.dumps(task_info)
    #send request
    try:
        logging.debug("post message to cloud service by requesting url %s: %s", cloud_url, task_info)
        request = tornado.httpclient.HTTPRequest(url=cloud_url,method="POST",body=task_info,request_timeout=20,connect_timeout=20)
        http_client = tornado.httpclient.AsyncHTTPClient()
        handler = PostTaskHandler(cb_func)
        http_client.fetch(request,handler.handle)
        return (True,None)
    except Exception,e:
        logging.warning("exception when sending request message to cloud service %s", str(e))
        return (False,error.ERROR_HTTP_REQUEST_INVALID)

class PostTaskHandler(object):
    def __init__(self,next_cb):
        self.__next_cb = next_cb
    def handle(self,response):
        next_cb = self.__next_cb
        if response.error:
            next_cb(False,error.ERROR_HTTP_REQUEST_TIMEOUT)
            return
        try:
            logging.debug("receive reponse from cloud service, now parse the response: %s", response.body)
            res = json.loads(response.body)
            success = res["success"]
            if success:
                task_id = res["data"]["task_id"]
                task_id = str(task_id)
                logging.debug("task id %s is found in the response", task_id)
                next_cb(True,task_id)
            else:
                err_msg = res["data"]["message"]
                logging.info("cloud service failed to process correspond request: %s", err_msg)
                next_cb(False,None)
        except Exception,e:
            logging.warning("exception when processing response from cloud service %s", str(e))
            next_cb(False,error.ERROR_JSON_SYNTAX_ERROR)
