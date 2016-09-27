#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This is http server which is a loop to dispatch incoming  requests.
    
"""
import tornado.httpserver
import tornado.ioloop
import logging
import time
from threading import Thread

from request_handler import RequestHandler

def mainloop():
    while True:
        try:
            time.sleep(8888)
        except KeyboardInterrupt:
            print "http Server is interrupted by administrator"
            return
        except Exception, err:
            _warn = "Exception happened in main thread %s " % (err) 
            print _warn 
        finally:
            pass
            
class HttpServer(Thread):
    def __init__(self, request_handler, port=80):
        # job management stuff
        Thread.__init__(self)
        self._request_handler = request_handler
        self._port            = port

    def _handle_request(self, request):
        try:
            _debug = "incoming request from %s " % (request.remote_ip)
            print "received: ", request 
            message = self._request_handler.handle_request(request)
            print "replied: ", message
            request.write(message)
            request.finish()
        except IOError, err:
            _err = "ioerror exception with %s" % (err)
            print _err 
        except Exception, err:
            _err = "exception with %s" % (err)
            print _err 

    def run(self):
        _critical = "thead with id = %d starts to run as http server thread" % (self.ident)
        print _critical 
        _info = "http server started with port = %d" % (self._port)
        print _info 
        http_server = tornado.httpserver.HTTPServer(self._handle_request, no_keep_alive = True)
        http_server.listen(int(self._port))
        tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    handler = RequestHandler()
    httpserver = HttpServer(handler, 8888)
    httpserver.daemon = True
    httpserver.start()
    mainloop()


