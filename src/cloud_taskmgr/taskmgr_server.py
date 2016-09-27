#!/usr/bin/python
# -*- coding:utf-8 -*- 

import tornado.httpserver
import tornado.ioloop
import routing
import mgmt
import error

class TaskmgrRequestHandler(object):
    ''' Callback handler to dispatch and handle request'''

    def __init__(self):
        self.__router = routing.Router()
        mgmt.initialize(self.__router)

    def handle_request(self,request):
        handler = self.__router.get_service_obj(request.path)
        if not handler:
            body = error.pack_errinfo_json(error.ERROR_HTTP_URL_NOT_SUPPORTED)
        else:
            body = handler(request)
        message = "HTTP/1.1 200 OK\r\nContent-Length:%d\r\n\r\n%s" % \
                                    (len(body),body)
        request.write(message)
        request.finish()

def start(port):
    request_handler = TaskmgrRequestHandler()
    http_server = tornado.httpserver.HTTPServer(request_handler.handle_request,no_keep_alive=True)
    http_server.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
    print "thread to quit:Main Thread"
    return True