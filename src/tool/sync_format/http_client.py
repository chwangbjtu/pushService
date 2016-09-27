# -*- coding:utf-8 -*-
from tornado import httpclient
from tornado import log
import json
 
class HttpClient(object):
    
    def __init__(self):
        self._http_client = httpclient.HTTPClient()

    def post_data(self, url, body):
        try:
            request = httpclient.HTTPRequest(url=url, method="POST", body=body)
            response = self._http_client.fetch(request)
            return (response.code, response.body)
        except httpclient.HTTPError,e:
            log.app_log.error("post error: [%s] [%s] [%s]" % (url, body, e))
            return ('', '')

    def get_data(self, url):
        try:
            request = httpclient.HTTPRequest(url=url, method="GET");
            response = self._http_client.fetch(request);
            if response:
                return (response.code, response.body);
        except httpclient.HTTPError,e:
            print "get error: [%s] [%s]" %(url, e)
            return ("", "");

 
if __name__ == "__main__":

    http_client = HttpClient()
    url = 'http://vpwind.flvcd.com/parse-fun.php?url=http://v.ku6.com/show/wX-zGBgijDESWRYIIQ4yyQ...html'
    ret = http_client.get_data(url)
    print ret
