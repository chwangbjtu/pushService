# -*- coding:utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import json
from tornado import log
import sys
import os
sys.path.append('.')
from common.conf import Conf
from common.auth import Auth
 
class PushHandler(tornado.web.RequestHandler):

    def initialize(self, conf, tq):
        self.conf = conf
        self.auth = Auth()
        self.tq = tq

    def check_body(self, body):
        essential_keys = ['origin', 'key', 'content']
        for k in essential_keys:
            if k not in body or not body[k]:
                return False

        return True

    def check_item(self, item):
        essential_keys = ['vid', 'url', 'title', 'tags', 'type']
        for k in essential_keys:
            if k not in item or not item[k]:
                return False

        return True

    def post(self):
        try:
            log.app_log.debug("PushHandler POST: %s" % self.request.body)
            #parse body
            try:
                body_json = json.loads(self.request.body)
                if not body_json:
                    ret_data = {'ret': 1, 'msg': 'body parse error'}
                    self.write(json.dumps(ret_data))
                    return
            except Exception as e:
                ret_data = {'ret': 1, 'msg': 'body parse error'}
                self.write(json.dumps(ret_data))
                return

            #check body parameter
            if not self.check_body(body_json):
                ret_data = {'ret': 1, 'msg': 'body parameter error'}
                self.write(json.dumps(ret_data))
                return

            site = body_json['origin']
            key = body_json['key']

            #verify key
            if not self.auth.auth_key(site, key):
                ret_data = {'ret': 1, 'msg': 'auth fail'}
                log.app_log.info('auth fail: %s, %s' % (site, key))
                self.write(json.dumps(ret_data))
                return

            #check content
            accept = []
            for item in body_json['content']:
                if self.check_item(item):
                    self.tq.add_tail({'site': site, 'info': item})
                    accept.append(item['vid'])

            #accept push
            ret_data = {'ret': 0, 'accept': accept}
            self.write(json.dumps(ret_data))

        except Exception as e:
            msg = 'PushHandler exception: %s' % e
            log.app_log.error(msg)
            ret_data = {'ret': 1, 'msg': 'unknown exception'}
            self.write(json.dumps(ret_data))

class HttpServer(object):
    
    def __init__(self, conf, task_queue):
        self.conf = conf
        self._app = tornado.web.Application([
            (r"/push", PushHandler, dict(conf=self.conf, tq=task_queue)),
        ])

    def __call__(self):
        log.app_log.debug('start http server: %s' % (self.conf.server_port))
        self._start_server()

    def _start_server(self):
        server = tornado.httpserver.HTTPServer(self._app)
        server.bind(self.conf.server_port)
        server.start(1)
        tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":

    from sender.mem_queue import MemQueue
    q = MemQueue('vps')
    conf = Conf()
    HttpServer(conf, q)()
