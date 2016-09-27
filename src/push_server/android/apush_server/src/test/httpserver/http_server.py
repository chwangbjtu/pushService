#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import tornado.httpserver
import tornado.ioloop
import urllib2
import json


class HttpServer:        
    _URL_PATH_PROGRESS = "/android/progress"
    def __init__(self):       
        self.__command_handlers = {}
        self.__command_handlers[self._URL_PATH_PROGRESS] = self.handle_progress

    def handle_progress(self, request):
        if request.method == "POST" and len(request.body) > 0:
            try:
                data = request.body
                print datetime.datetime.now()
                print data

            except Exception, e:
                print "err:",e
        else:
            return "path or method error"
        msg = {}
        msg["retcode"] = "200"
        msg["retmsg"] = "ok"
        
        return json.dumps(msg)

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


if __name__ == "__main__":
    taskserver = HttpServer()
    taskserver.start(6600)
