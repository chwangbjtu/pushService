# -*-coding:utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from handler import regist_new
from handler import delete_tk
from handler import regist_v1
from handler import regist_v2

from tornado.options import define, options
define("port", default = 8000, help = "run on the given port", type = int)
            
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
            (r"/app/register", regist_new.AppRegisterHandler),
            (r"/service/del_token", delete_tk.DelDeviceHandler),
            (r"/api/regist.php", regist_v1.AppRegisterV1Handler),
            (r"/v2/push/regist", regist_v2.AppRegisterV2Handler)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    