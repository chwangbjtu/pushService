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
from db.db_connect import MysqlConnect
from db.episode_dao import EpisodeDao
from db.episode_status_dao import EpisodeStatusDao
from common.util import Util
 
class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        log.app_log.debug("VersionHandler: GET")
        self.write("Version 0.1")
 
class StatisticHandler(tornado.web.RequestHandler):
    def get(self):
        log.app_log.debug("StatisticHandler: GET")
        self.write("Statistic")

class SendEpisodeHandler(tornado.web.RequestHandler):
    def initialize(self, q_mgr,ep_dao):
        self._q_mgr = q_mgr
        #self._ep_dao = EpisodeDao(self._db_conn)
        self._ep_dao = ep_dao

    def get(self):
        log.app_log.debug("SendEpisodeHandler: GET")
        show_id = self.get_query_argument('sid')
        audit = self.get_query_argument('audit', '1')
        priority = self.get_query_argument('priority', '')
        force = self.get_query_argument('force', '0')
        episode = self._ep_dao.get_episode(show_id)
        if episode:
            para = {}
            if audit:
                episode['audit'] = str(audit)
                para['audit'] = str(audit)
            if priority:
                episode['priority'] = str(priority)
                para['priority'] = str(priority)
            if force:
                episode['force'] = str(force)

            para['id'] = episode['id']
            self._q_mgr.get_queue('ep_q').add_tail({'data': episode, 'origin': 0})
            self._ep_dao.set_control_info(para)

            self.write('{"ret": "0"}')
        else:
            self.write('{"ret": "1"}')

class PushHandler(tornado.web.RequestHandler):
    def initialize(self, q_mgr,ep_dao):
        self._q_mgr = q_mgr
        self._ep_dao = ep_dao

    def check_body(self, body):
        essential_keys = ['user', 'key', 'content']
        for k in essential_keys:
            if k not in body or not body[k]:
                return False

        return True

    def check_item(self, item):
        essential_keys = ['vid', 'url', 'title', 'category', 'type']
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

            uid = self._ep_dao.get_uid(body_json['user'])
            site_id = self._ep_dao.get_site_id(body_json['user'])

            #verify user
            if not uid:
                ret_data = {'ret': 1, 'msg': 'auth fail'}
                log.app_log.info('auth fail: %s' % (body_json['user'],))
                self.write(json.dumps(ret_data))
                return

            #check content
            accept = []
            for item in body_json['content']:
                if self.check_item(item):
                    episode = {}
                    episode['uid'] = uid
                    episode['site_id'] = site_id
                    episode['type'] = item['type']
                    episode['show_id'] = item['vid']
                    episode['url'] = item['url']
                    episode['title'] = item['title']
                    episode['category'] = item['category']
                    episode['audit'] = 0
                    if 'priority' in item:
                        episode['priority'] = item['priority']
                    if 'audit' in item:
                        episode['audit'] = item['audit']
                    if 'tag' in item:
                        episode['tag'] = item['tag']
                    if 'description' in item:
                        episode['description'] = item['description']
                    if 'pub_time' in item:
                        episode['upload_time'] = item['pub_time']

                    if self._ep_dao.insert_customer_episode(episode):
                        #log.app_log.debug('%s' % json.dumps(episode))
                        accept.append(item['vid'])

            #accept push
            ret_data = {'ret': 0, 'accept': accept}
            self.write(json.dumps(ret_data))

        except Exception as e:
            msg = 'PushHandler exception: %s' % e
            log.app_log.error(msg)
            ret_data = {'ret': 1, 'msg': 'unknown exception'}
            self.write(json.dumps(ret_data))

class UpdateBlacklistHandler(tornado.web.RequestHandler):
    
    def initialize(self, http_pipe):
        self._http_pipe = http_pipe

    def get(self):
        log.app_log.debug("UpdateBlacklistHandler: GET")
        try:
            op = self.get_argument("op", "")
            content = Util.unquote(self.get_argument("content", ""))
            log.app_log.debug("current op type: %s, and content: %s" % (op, content))

            res = {'ret': '0'}

            if op == "reload":
                res = self.send_op(op, '')
            else:
                if content:
                    if op == "add" or op == "filter":
                        res = self.send_op(op, content)
                    else:
                        res = {'ret': '1', 'msg': 'op not support'}
                else:
                    res = {'ret': '1', 'msg': 'empty content'}

            self.write(json.dumps(res))

        except Exception, e:
            log.app_log.error("update blacklist exception: %s " % traceback.format_exc())
            self.write(json.dumps({'ret': '1', 'msg': str(e)}))
    
    def send_op(self, op, content):
        self._http_pipe.send(json.dumps({'op': op, 'content': content}))
        res = self._http_pipe.recv()
        return res

class DownloadfinishHandler(tornado.web.RequestHandler):
    def initialize(self, q_mgr,ep_dao):
        self._q_mgr = q_mgr
        #self._ep_dao = EpisodeStatusDao(self._db_conn)
        self._ep_dao = ep_dao

    def post(self):
        log.app_log.debug("DownloadfinishHandler: POST")
        log.app_log.debug("body: %s" % (self.request.body,))
        try:
            data = json.loads(self.request.body)
            turl = data["url"]
            ids = data["id"]
            result = data["result"]
            ret = '2'
            if result == "0":#succ
                ret = '1'
            
            idnum = len(ids)
            for i in range(idnum):
                id = ids[i]
                step_id = None
                status = None
                (step_id,status) = self._ep_dao.get_step_status(id)
                if step_id:
                    if 10 >= int(step_id) and int(status) != 1:
                        self._ep_dao.update_status(id,step_id,ret,turl)
        except Exception, e:
            log.app_log.error("insert status exception: %s " % traceback.format_exc())

        self.write('{"ret": "0"}')

class HttpServer(object):
    
    def __init__(self, port, q_mgr, http_pipe):
        self._port = port
        self._db_conn = MysqlConnect()
        self._app = tornado.web.Application([
            (r"/query/version", VersionHandler),
            (r"/query/statistic", StatisticHandler),
            (r"/op/sendepisode", SendEpisodeHandler, dict(q_mgr=q_mgr, ep_dao=EpisodeDao(self._db_conn))),
            (r"/maze/download_finish", DownloadfinishHandler, dict(q_mgr=q_mgr,ep_dao=EpisodeStatusDao(self._db_conn))),
            (r"/op/updateblacklist", UpdateBlacklistHandler, dict(http_pipe=http_pipe)),
            (r"/op/push", PushHandler, dict(q_mgr=q_mgr, ep_dao=EpisodeDao(self._db_conn))),
        ])

    def __call__(self):
        log.app_log.debug('start http server: %s' % (self._port))
        self._start_server()

    def _start_server(self):
        server = tornado.httpserver.HTTPServer(self._app)
        server.bind(self._port)
        server.start(1)
        tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":

    HttpServer(8100)()
