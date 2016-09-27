#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""send http msg""" 
import urllib2
import tornado.httpclient
import json

def post(ip, port, url, strinfo):
    """http visitor ,method post"""
    _opener = urllib2.build_opener()
    response = None
    code = -1
    try:
        exserver_url = "http://%s:%s%s" % (ip, port, url)
        response = _opener.open(exserver_url, strinfo, timeout = 20)
        code = response.getcode()
    except Exception, error:
        print 'post has err with _opener.open, error = ', error
        return (code, error.message)
    else:
        content = response.read()
        response.close()
        return (code, content)


def get(ip, port, url):
    """http visitor ,method get"""
    _opener = urllib2.build_opener()
    response = None
    code = -1
    try:
        _url = "http://%s:%s%s" % (ip, port, url)
        response = _opener.open(_url, timeout = 15)
        code = response.getcode()
        print 'code:', code
    except Exception, error:
        print 'get has err with _opener.open, error = ', error
        return (code, error.message)
    else:
        content = response.read()
        print "get response:", content
        response.close()
        return (code, content)


def post_crane_task(ip , port, data_info):
    method = "/crane/?cmd=examresult"
    url = "http://%s:%s%s" % (ip, port, method)
    try:
        request = tornado.httpclient.HTTPRequest(url,method="POST",body=data_info,request_timeout=20,connect_timeout=20)
        response = client.fetch(request)
    except tornado.httpclient.HTTPError,e:
        print 'post_crane_task error.',e
        #masterlogging.error(logginghelper.LogicLog("None","RequireTask","fail",e.message))
        return False
    return True
    
def post_audit_task(ip, port, audit_result):
    method = "/maze/audit"
    url = "http://%s:%s%s" % (ip, port, method)
    try:
        request = tornado.httpclient.HTTPRequest(url,method="POST",body=audit_result,request_timeout=20,connect_timeout=20)
        response = tornado.httpclient.HTTPClient().fetch(request)
        result = json.loads(response.body)
        if result.has_key('result') and result['result'] == 'ok':
            return True
        else:
            return False
            
    except tornado.httpclient.HTTPError,e:
        #print 'post_audit_task error.',e
        #masterlogging.error(logginghelper.LogicLog("None","RequireTask","fail",e.message))
        return False
    return True