# -*- coding: utf-8 -*-
from tornado import httpclient
import json

class HttpClient(object):
    def __init__(self):
        self._http_client = httpclient.HTTPClient();

    def post_data(self, url, body):
        try:
            request = httpclient.HTTPRequest(url=url, method="POST", body=body, connect_timeout=120, request_timeout=120);
            response = self._http_client.fetch(request);
            if response:
                return (response.code, response.body);
        except httpclient.HTTPError,e:
            #print "post error: [%s] [%s] [%s]" %(url, body, e)
            return ("", "");

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
    import sys
    sys.path.append(".");
    # from common.conf import Conf
    #content = {"origin":"upload", "describe":"1414", "uid":1, "vid":"XNzIxNzUyMDAw", "title":u"侣行 第二季", "tags":u"t|a|g", "site":"cntv", "priority":7, "channel":u"example|example_1|example_2"};
    hc = HttpClient();
    #res = hc.post_data('http://192.168.16.118:6813/maze/addtask', json.dumps(content));
    res = hc.get_data("http://macross.funshion.com:27777/api/?cli=video&cmd=get_video_info_by_hashid&hashid=B1BBBD9B790848F053F7351F1D6245EA16FAF8F2");
    if res:
        print "return %s: %s" % (res[0], res[1])
