# -*-coding:utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import log
import json
from handler import regist_new
from handler import delete_tk
from handler import regist_v1
from handler import regist_v2
from handler import loadmsg
from handler import getlastmsg
from common.conf import Conf
from tornado.options import define, options
define("port", default = 18000, help = "run on the given port", type = int)
            
if __name__ == "__main__":
    #tornado.options.parse_command_line()
    log.app_log.info("start server, port is:%s" % Conf.server_port)
    app = tornado.web.Application(
        handlers = [
            (r"/v2/app/register", regist_new.AppRegisterHandler),
            (r"/v2/service/del_token", delete_tk.DelDeviceHandler),
            (r"/v2/app/getlastmsg", getlastmsg.GetLastMsgHandler),
            (r"/v2/app/loadmsg", loadmsg.LoadMsgHandler)
        ]
    )
    '''
    sockets = tornado.netutil.bind_sockets(Conf.server_port)
    tornado.process.fork_processes(Conf.process_num)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()
    '''
    http_server = tornado.httpserver.HTTPServer(app,idle_connection_timeout=Conf.idle_connection_timeout)
    http_server.listen(Conf.server_port)
    #http_server.bind(Conf.server_port)
    #http_server.start(Conf.process_num)
    tornado.ioloop.IOLoop.instance().start()
    
