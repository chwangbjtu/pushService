# -*- coding:utf-8 -*-
from tornado import httpclient
import json
import logging
 
class HttpClient(object):
    
    def __init__(self):
        self._http_client = httpclient.HTTPClient()

    def post_data(self, url, body):
        try:
            request = httpclient.HTTPRequest(url=url, method="POST", body=body)
            response = self._http_client.fetch(request)
            return (response.code, response.body)
        except httpclient.HTTPError,e:
            logging.info("post error: [%s] [%s] [%s]" % (url, body, e))
            return ('', '')
 
