# -*- coding:utf-8 -*-
import sys
import tornado.httpclient

if __name__ == "__main__":

    try:
        #file_object = open('/tmp/t2.jpg')
        #file_object = open('/tmp/dsc04403.jpg')
        #file_object = open('/tmp/tupian.jpg')
        file_object = open('/tmp/error1.jpg')
        all_the_text = file_object.read( )
        file_object.close( )
        print len(all_the_text)

        http_client = tornado.httpclient.HTTPClient()
        url = "http://192.168.16.113:8099/upload?width=120&height=240"
        #url = "http://192.168.16.154:7889/upload?width=120&height=240"
        parastr = all_the_text
        http_request = tornado.httpclient.HTTPRequest(url=url,body=parastr,method='POST',connect_timeout=5,request_timeout=600)
        http_response = http_client.fetch(http_request)
        res = http_response.body
        print res

    except Exception as e:
        print "err",e
