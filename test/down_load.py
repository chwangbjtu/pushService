#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import json
import time
import urllib2
import urllib2_thread_wrapper
import httplib
import httplib2
import url_helper

def download(url, filepath, task_id):
    """download methord"""
    res = 0
    length = 0
    recv_info_size = 0
    if not url or not filepath:
        return res
    try:
        req = None
        f = None
        f = None
        try:
            req = urllib2.Request(url)
            r = urllib2.urlopen(req, None, timeout = 60)
            recv_info = r.info()
            print 'recv info task_id = %d, recv_info = \n%s' % (task_id, str(recv_info))
            if 'Content-Type' not in recv_info:
                print "not find Content-Type"
                raise Exception()
            if 'Content-Length' not in recv_info:
                print "not find Content-Length"
                raise Exception()
            if 'text/html' == recv_info['Content-Type']:
                raise Exception()
            recv_info_size = int(recv_info['Content-Length'])
            f = open(filepath, 'wb')
        except:
            print 'urllib2 connect error or open file for reading error'
            exception = traceback.format_exc()
            raise Exception()
       
 
        try:
 
            while True:
                recv_buffer = r.read(1024*256)
                if 0 == len(recv_buffer):
                    break
                f.write(recv_buffer)
 
 
 
        except:
            print 'reading or writing error'
            exception = traceback.format_exc()
            print exception
            raise Exception()
        finally:
            f.close()
 
        real_write_size = os.path.getsize(utf8_to_local(filepath))
        if real_write_size != recv_info_size:
            print 'broker Downloadthread: download function error, task_id = %d, real write size: %d\nrecv_info_size: %d' % (task_id, real_write_size, recv_info_size)
            raise Exception()
    except:
        exception =  traceback.format_exc()
        print exception
        res = -1
    finally:
        return res

