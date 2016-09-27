# -*- coding:utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import log
import traceback
import sys
import json
sys.path.append('.')
from common.conf import Conf
 
class HelperHandler(tornado.web.RequestHandler):
    def initialize(self, api_handler):
        self._api_handler = api_handler

    def get(self):
        #api = self.get_query_argument('api', '')
        api = 'parse'
        log.app_log.debug("GET helper api: %s" % api)

        if api in self._api_handler:
            #self.write('{"ret": "0"}')
            handler = self._api_handler[api]
            url = self.get_query_argument('url', '')
            res = handler.handle(url)
            self.write(res)
        else:
            self.write('{"ret": "1"}')

class HttpServer(object):
    
    def __init__(self, port):
        self._port = port
        self._api_handler = {}
        self._app = tornado.web.Application([
            (r"/parse", HelperHandler, dict(api_handler=self._api_handler)),
        ])

    def __call__(self):
        self.start()

    def register_api(self, api, handler):
        self._api_handler[api] = handler

    def start(self):
        log.app_log.debug('start http server: %s' % (self._port))
        server = tornado.httpserver.HTTPServer(self._app)
        server.bind(self._port)
        server.start(1)
        tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":

    class Test(object):
        def handle(self):
            log.app_log.debug('handle test')

    srv = HttpServer(8100)
    srv.register_api('test', Test())
    srv.start()
