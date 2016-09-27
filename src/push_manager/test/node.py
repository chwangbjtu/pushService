# -*- coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.')
from common.http_client import HttpClient

class Test():

    def test_server_add_node(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/server/add_node'
            data = {}
            push_1 = {"type":"push", "ip":"192.168.16.113"}
            data['node'] = [push_1]
            body = json.dumps(data)
            res = http_client.post_data(url, body)
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def test_server_get_node(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/server/get_node?type=push'
            res = http_client.get_data(url) 
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def test_server_del_node(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/server/del_node'
            data = {}
            push_1 = {"type":"push", "ip":"192.168.16.113"}
            data['node'] = [push_1]
            body = json.dumps(data)
            res = http_client.post_data(url, body)
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == '__main__':
    test = Test()
    test.test_server_add_node()
    #test.test_server_get_node()
    #test.test_server_del_node()
