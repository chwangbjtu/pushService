#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""send http msg""" 
import urllib2

def post(ip, port, url, strinfo):
    """http visitor ,method post"""
    _opener = urllib2.build_opener()
    response = None
    code = -1
    try:
        exserver_url = "http://%s:%s%s" % (ip, port, url)
        response = _opener.open(exserver_url, strinfo, timeout = 5)
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
        response = _opener.open(_url, timeout = 5)
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

if __name__ == "__main__":
    import os
    ip = '192.168.16.34'
    port = 6800
    '''
    surl = "/ems/addtaskstatus"
    body = "{\"tid\":\"123223\",\"step\":\"upload\", \"status\":1}"
    res = post(ip, port, surl, body)
    print '1 add status: ', res

    body = "{\"tid\":\"123224\",\"step\":\"forwards\", \"status\":1}"
    res = post(ip, port, surl, body)
    print '2 add status: ', res

    body = "{\"tid\":\"123223\",\"step\":\"taskmanager\", \"status\":2}"
    res = post(ip, port, surl, body)
    print '3 add status: ', res


    surl = "/ems/gettaskstatus?tid=123223"
    res = get(ip, port, surl)
    print 'get status: ', res
    '''
    surl = "/ems/upload_url"
    body = "{\"tid\":\"1365676334.31\",\"url\":\"http://192.168.16.34:7777/a.mp4\"}"
    res = post(ip, port, surl, body)
    print '1 add status: ', res

    surl = "/ems/gettaskstatus?tid=1365676334.31"
    res = get(ip, port, surl)
    print 'get status: ', res

    os.system("PAUSE")

     
