#!/usr/bin/python
# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import urllib2
from urllib import urlencode
import json
import logging
import logging.handlers
import etc
from task_dao import TaskDao
import push_maze
import os
import sys
import md5
import MySQLdb

class HttpServer:        
    _download_add =     "/add_download"
    _get_task =         "/get_task"
    _update_task =      "/update_task"
    _get_server =       "/get_server"
    _get_url      =     "/get_url"
    _upload_start =     "/maze/upload_start"
    _upload_finish  =   "/maze/upload_finish"
    _HTTP_RESP1 = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:"
    def __init__(self):
        #self.__db = db_connector.db_connector()
        self.__db = TaskDao()
        self.__pusher = push_maze.push_maze()
        self.__pusher.load_msg()
        self.__pusher.start()
        self.__command_handlers = {}
        self.__command_handlers[self._download_add] = self.download_add
        self.__command_handlers[self._get_task] = self.get_task
        self.__command_handlers[self._update_task] = self.update_task
        #upload
        self.__command_handlers[self._get_server] = self.get_server
        self.__command_handlers[self._get_url] = self.get_url
        self.__command_handlers[self._upload_start] = self.upload_start
        self.__command_handlers[self._upload_finish] = self.upload_finish

    def download_add(self, request):
        resp={}
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                try:
                    logging.info("download_add: " + data)
                    djson = json.loads(data)
                    vid = djson["vid"]
                    site = djson["site"]
                    src_url = djson["src_url"]
                    if "task_id" in djson:
                        task_id = djson["task_id"]
                    else:
                        vidsite = str(vid) + str(site)
                        tmd5 = md5.new()
                        tmd5.update(vidsite)
                        task_id = str(tmd5.hexdigest())
                    id = djson["id"]
                    priority = str(djson["priority"])
                    op = djson["op"]

                    #resp["task_id"] = task_id

                    #self.__db.insert(task_id,site,vid,priority,op)
                    did = ""
                    did = self.__db.insert(task_id,id,site,vid,priority,op,src_url)
                    resp["did"] = did

                    logging.info("download_add: " + str(task_id))
                    resp["ret"] = "0"
                    resp["msg"] = ""
                except Exception,e:
                    logging.error("download_add task_id is:" + task_id + " error:" + str(e))
                    resp["ret"] = "1"

            except Exception, e:
                logging.error("download_add error:" + str(e))
                resp["ret"] = "1"
        else:
            logging.error("download_add, request methon is not POST or request body is empty")
            resp["ret"] = "1"
        
        return json.dumps(resp)

    def get_task(self, request):
        worker_ip = request.remote_ip
        resp={}
        resp["ret"] = "1"
        task_id = None
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                try:
                    logging.info("get_task: " + data)
                    djson = json.loads(data)
                    op = djson["op"]
                    site = None
                    if "site" in djson:
                        site = djson["site"]
                    task_id = None
                    vid = None
                    #tsite = site
                    (task_id,tsite,vid,src_url) = self.__db.get_task(op,site,worker_ip)
                    site = tsite
                    logging.info("get_task: " + str(data))
                    if task_id and site and vid:
                        #if len(task_id) != 0 and len(site) != 0 and len(vid) != 0:
                        resp["task_id"] = task_id
                        resp["site"] = site
                        resp["vid"] = vid
                        resp["src_url"] = src_url
                        resp["ret"] = "0"
                    
                except Exception,e:
                    logging.error("get_task error, task_id is:" + task_id + " error:" + str(e))
                    resp["ret"] = "1"

            except Exception, e:
                logging.error("get_task error:" + str(e))
                resp["ret"] = "1"
        else:
            logging.error("get_task,request methon is not POST or request body is empty")
            resp["ret"] = "1"
        
        return json.dumps(resp)

    def update_task(self, request):
        resp={}
        resp["ret"] = "0"
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                try:
                    logging.info("update_task: " + data)
                    djson = json.loads(data)
                    task_id = djson["task_id"]
                    #site = djson["site"]
                    url = djson["url"]
                    ret = djson["ret"]
                    status = 3#sucess
                    if ret != "0":
                        status = 2
                        logging.debug("update_task ret is:" + str(ret))
                    elif len(url) == 0:
                        resp["ret"] = "1"
                        resp["msg"] = "url len is 0"
                        logging.error("task_id is:" + task_id + ",url len is 0")
                        return json.dumps(resp)
                        
                    logging.debug("debug")
                    tres = self.__db.update_db(task_id,status,url)
                    logging.debug("debug")
                except Exception,e:
                    logging.error("update_task error, task_id is:" + task_id + " error:" + str(e))

            except Exception, e:
                logging.error("update_task error:" + str(e))
        else:
            logging.error("update_task,request methon is not POST or request body is empty")

        return json.dumps(resp)

    def get_server(self, request):
        resp={}
        resp["ret"] = "1"
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                logging.info("get_server: " + data)
                djson = json.loads(data)
                op = djson["op"]
                logging.info("befor")
                (ip,port) = self.__db.get_server(op)
                logging.info("after")

                if ip and port:
                    resp["ip"] = ip
                    resp["port"] = port
                    resp["ret"] = "0"

            except Exception, e:
                logging.error("get_server error:" + str(e))
                resp["ret"] = "1"
        else:
            logging.error("get_server,request methon is not POST or request body is empty")
            resp["ret"] = "1"
        
        return json.dumps(resp)

    def get_url(self, request):
        print request.remote_ip
        resp={} 
        resp["ret"] = "1"
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                logging.info("get_url: " + data)
                djson = json.loads(data)
                taskid = djson["taskid"]
                logging.info("befor")
                (url) = self.__db.get_url(taskid)
                logging.info("after")

                if url:
                    resp["url"] = url
                    resp["ret"] = "0"

            except Exception, e:
                logging.error("get_url error:" + str(e))
                resp["ret"] = "1"
        else:
            logging.error("get_url,request methon is not POST or request body is empty")
            resp["ret"] = "1"

        return json.dumps(resp)

    def upload_start(self, request):
        resp={}
        resp["ret"] = "1"
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                logging.info("upload_start: " + data)
                djson = json.loads(data)
                task_id = djson["task_id"]
                file = djson["file"]
                file_name = djson["file_name"]
                file_size = djson["file_size"]
                file_url  = djson["file_url"]
                uid = djson["uid"]
                hashid = djson["hashid"]
                logging.info("")

                self.__db.upload_start(task_id,file_name,file_size,file_url,uid,hashid)
                logging.info("")
                resp["ret"] = "0"

            except Exception, e:
                logging.error("upload_start error:" + str(e))
                resp["ret"] = "1"
        else:
            logging.error("upload_start,request methon is not POST or request body is empty")
            resp["ret"] = "1"

        return json.dumps(resp)

    def upload_finish(self, request):
        resp={}
        resp["ret"] = "1"
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                logging.info("upload_finish: " + data)
                djson = json.loads(data)
                task_id = djson["task_id"]
                file = djson["file"]
                file_name = djson["file_name"]
                file_size = djson["file_size"]
                file_url  = djson["file_url"]
                uid = djson["uid"]
                hashid = djson["hashid"]

                logging.info("befor finish")
                self.__db.upload_finish(task_id,file_name,file_size,file_url,uid,hashid)
                logging.info("after finish")
                resp["ret"] = "0"
            
            except Exception, e:
                logging.error("upload_finish error:" + str(e))
                resp["ret"] = "1"
        else:
            logging.error("upload_finish,request methon is not POST or request body is empty")
            resp["ret"] = "1"

        return json.dumps(resp)

    def handle_request(self, request):
        if not self.__command_handlers.has_key(request.path.lower()):
            message = "HTTP/1.1 404 Not Found\r\nConnection:Close\r\nContent-Length:0\r\n\r\n"
        else:
            url = request.path.lower()
            handler = self.__command_handlers[url]
            body = handler(request)
            message = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:%d\r\n\r\n%s" % (
                                                                  len(body), body)
        request.write(message)
        request.finish()

    def start(self, port):
        http_server = tornado.httpserver.HTTPServer(self.handle_request, no_keep_alive = False)
        http_server.listen(int(port))
        tornado.ioloop.IOLoop.instance().start()
        return True

    def handle_request(self, request):
        if not self.__command_handlers.has_key(request.path.lower()):
            message = "HTTP/1.1 404 Not Found\r\nConnection:Close\r\nContent-Length:0\r\n\r\n"
        else:
            url = request.path.lower()
            handler = self.__command_handlers[url]
            body = handler(request)
            message = "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:%d\r\n\r\n%s" % (
                                                                  len(body), body)
        request.write(message)
        request.finish()

    def start(self, port):
        http_server = tornado.httpserver.HTTPServer(self.handle_request, no_keep_alive = False)
        http_server.listen(int(port))
        tornado.ioloop.IOLoop.instance().start()
        return True
