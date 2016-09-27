# -*- coding:utf-8 -*-
import time
import traceback
import tornado
from tornado import ioloop
from tornado import log
from tornado import web
from tornado import httpserver

import sys
sys.path.append('.')
from conf import Conf
from common.util import PushType
from common.util import check_mongo, check_mysql 
from service.push_ghost import PushGhost

class HttpServer(object):
    def __init__(self, port):
        self._port = port
        self._api_handler = {}

    def start(self):
        log.app_log.info('start http server: %s' % (self._port))
        apps = []
        for api in self._api_handler:
            apps.append((api, self._api_handler[api]))
        self._app = web.Application(apps)
        server = httpserver.HTTPServer(self._app, no_keep_alive=False)
        server.bind(self._port)
        server.start(1)
        ioloop.IOLoop.instance().start()

    def register_api(self, api, handler):
        self._api_handler[api] = handler

class PoHandler(web.RequestHandler):

    def get(self, path):
        from po.cancel_handler import CancelHandler
        from po.progress_handler import ProgressHandler
        try:
            if 'cancel' == path:
                msgid = self.get_query_argument('msgid', '')
                cancel_handler = CancelHandler()
                para = {'msgid':msgid}
                res = cancel_handler.handle(para=para)
                self.write(res)
            elif 'progress' == path:
                msgid = self.get_query_argument('msgid', '')
                progress_handler = ProgressHandler()
                para = {'msgid':msgid}
                res = progress_handler.handle(para=para)
                self.write(res)
            else:
                self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def post(self, path):
        from po.push_handler import PushHandler
        try:
            if 'push_all' == path:
                push_handler = PushHandler()
                para = {'push_type':PushType.All}
                body = self.request.body
                res = push_handler.handle(para=para, body=body)
                self.write(res)
            elif 'push_test' == path:
                push_handler = PushHandler()
                para = {'push_type':PushType.Test}
                body = self.request.body
                res = push_handler.handle(para=para, body=body)
                self.write(res)
            else:
                self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class ServiceHandler(web.RequestHandler):

    def get(self, path):
        from service.get_task_handler import GetTaskHandler
        try:
            if 'get_task' == path:
                total = self.get_query_argument('total', '')
                para = {'total':total}
                get_task_handler = GetTaskHandler()
                res = get_task_handler.handle(para=para)
                self.write(res)
            else:
                self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def post(self, path):
        from service.rep_task_handler import RepTaskHandler
        try:
            if 'rep_task' == path:
                rep_task_handler = RepTaskHandler()
                body = self.request.body
                res = rep_task_handler.handle(body=body)
                self.write(res)
            else:
                self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class ServerHandler(web.RequestHandler):

    def get(self, path):
        from server.get_node_handler import GetNodeHandler
        try:
            if 'get_node' == path:
                type = self.get_query_argument('type', '')
                para = {'type':type}
                get_node_handler = GetNodeHandler()
                res = get_node_handler.handle(para=para)
                self.write(res)
            else:
                self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def post(self, path):
        from server.add_node_handler import AddNodeHandler
        from server.del_node_handler import DelNodeHandler
        try:
            if 'add_node' == path:
                add_node_handler = AddNodeHandler()
                body = self.request.body
                res = add_node_handler.handle(body=body)
                self.write(res)
            elif 'del_node' == path:
                del_node_handler = DelNodeHandler()
                body = self.request.body
                res = del_node_handler.handle(body=body)
                self.write(res)
            else:
                self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

class AndroidHandler(web.RequestHandler):

    def get(self, path):
        try:
            self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def post(self, path):
        from android.progress_handler import ProgressHandler
        try:
            if 'progress' == path:
                progress_handler = ProgressHandler()
                #ip = self.request.remote_ip
                ip = self.request.headers.get("X-Forwarded-For", "")
                body = self.request.body
                para = {'ip':ip}
                res = progress_handler.handle(para=para, body=body)
                self.write(res)
            else:
                self.write('404:not found')
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":
    if not check_mongo():
        log.app_log.info('environment is not ready, check it...')
        exit(1);
    log.app_log.info('push ghost server start...')
    http_server = HttpServer(Conf.server_port)
    push_ghost = PushGhost()
    push_ghost.start()
    #如果前端有加反向代理，需用如下方式
    #http_server = HttpServer(Conf.server_port, xheaders=True)
    http_server.register_api('.*/po/(\w+)', PoHandler)
    http_server.register_api('.*/service/(\w+)', ServiceHandler)
    http_server.register_api('.*/server/(\w+)', ServerHandler)
    http_server.register_api('.*/android/(\w+)', AndroidHandler)
    log.app_log.info('tornado server start...')
    http_server.start()

    push_ghost.join()
