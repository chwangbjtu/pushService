# -*- coding:utf-8 -*-
import json
import traceback
from tornado import log
import time
import sys
sys.path.append('.')
from common.http_client import HttpClient

class Test():

    def test_po_push(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/po/push_all'
            #url = 'http://127.0.0.1:8990/v2/po/push_test'
            data = {}
            msgid = '300203'
            data['msgid'] = msgid
            data['start_time'] = str(int(time.time()) + 30)
            msg_summary = {"msgid":msgid, "title":u"test1", "content":u"test3"}
            msg_detail = {"msgid":msgid,"title":u"test2","content":u"test2", 
                    "badge":"0", "id":"209450", "mtype":"mplay", "poster":"http://img.funshion.com/sdw?oid=e815bd2f621a63474d27042c28281f3e&w=0&h=0",
                    "url":"http://jsonfe.funshion.com/media/?cli=aphone&ver=1.5.1.3&sid=0002&mid=300705", "num":"1", "still":"http://www.fun.tv",
                    "style":"1"}
            payload = {"summary":json.dumps(msg_summary), "detail":json.dumps(msg_detail)}
            data['payload'] = payload
            body = json.dumps(data)
            res = http_client.post_data(url, body)
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            
    def test_po_push_test(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/po/push_test'
            data = {}
            msgid = '400184'
            data['msgid'] = msgid
            data['start_time'] = str(int(time.time()) + 5)
            data['token'] = []
            data['token'].append({'platform':'android', 'app_name':'aphone', 'id':'aacc'})
            msg_summary = {"msgid":msgid, "title":u"test1", "content":u"test3"}
            msg_detail = {"msgid":msgid,"title":u"test2","content":u"test2", 
                    "badge":"0", "id":"209450", "mtype":"mplay", "poster":"http://img.funshion.com/sdw?oid=e815bd2f621a63474d27042c28281f3e&w=0&h=0",
                    "url":"http://jsonfe.funshion.com/media/?cli=aphone&ver=1.5.1.3&sid=0002&mid=300705", "num":"1", "still":"http://www.fun.tv",
                    "style":"1"}
            payload = {"summary":json.dumps(msg_summary), "detail":json.dumps(msg_detail)}
            data['payload'] = payload
            body = json.dumps(data)
            res = http_client.post_data(url, body)
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def test_po_progress(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/po/progress?msgid=11126'
            res = http_client.get_data(url) 
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def test_po_cancel(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/po/cancel?msgid=11126'
            res = http_client.get_data(url) 
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def test_service_get_task(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/service/get_task?total=1000'
            res = http_client.get_data(url) 
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def test_service_rep_task(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/v2/service/rep_task'
            data = {}
            data['msg_id'] = '11126'
            data['pull_id'] = '192.168.16.155:4972:1'
            data['total'] = '2'
            data['success'] = '1'
            data['fail'] = '1'
            body = json.dumps(data)
            res = http_client.post_data(url, body)
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def test_android_report(self):
        try:
            http_client = HttpClient() 
            url = 'http://127.0.0.1:8990/android/progress'
            data = {}
            data['result'] = []
            detail = {}
            detail['msgid'] = '300113'
            detail['total_conn'] = 100
            detail['success'] = 97
            detail['user_num'] = 100
            data['result'].append(detail)
            body = json.dumps(data)
            res = http_client.post_data(url, body)
            print res
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 

if __name__ == '__main__':
    test = Test()
    test.test_po_push()
    #test.test_po_push_test()
    #test.test_service_get_task()
    #test.test_service_rep_task()
    #test.test_po_cancel()
    #test.test_po_progress()
    #test.test_android_report()
