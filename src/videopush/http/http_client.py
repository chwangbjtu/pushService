# -*- coding:utf-8 -*-
from tornado import httpclient
from tornado import log
import json
 
class HttpClient(object):
    
    def __init__(self):
        self._http_client = httpclient.HTTPClient()

    def get_data(self, url):
        try:
            request = httpclient.HTTPRequest(url=url, method="GET")
            response = self._http_client.fetch(request)
            return (response.code, response.body)
        except httpclient.HTTPError,e:
            log.app_log.error("post error: [%s] [%s]" % (url, e))
            return ('', '')
 

    def post_data(self, url, body):
        try:
            request = httpclient.HTTPRequest(url=url, method="POST", body=body)
            response = self._http_client.fetch(request)
            return (response.code, response.body)
        except httpclient.HTTPError,e:
            log.app_log.error("post error: [%s] [%s] [%s]" % (url, body, e))
            return ('', '')
 
if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from common.conf import Conf

    content = {"task_id": "111"}
    hc = HttpClient()
    res = hc.post_data('http://192.168.16.118:6813/maze/transcode_start', json.dumps(content))
    if res:
        log.app_log.debug("return %s: %s" % (res[0], res[1]))
