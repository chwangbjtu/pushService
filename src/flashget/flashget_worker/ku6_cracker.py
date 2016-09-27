#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import urllib2_thread_wrapper
import url_helper

def get_json_from_id(id):
    json_url = "http://v.ku6.com/fetchVideo4Player/%s.html" % id
    try:
        opener = urllib2_thread_wrapper.get_opener()
        response = opener.open(json_url, timeout = 30)
        content = response.read()
    except Exception,e:
        return None
    return content


def get_video_url_and_type(jsoninfo):
    urls = []
    try:
        result = json.loads(jsoninfo)
        video_url = result["data"]["f"]
        prev_pos = 0
        while prev_pos != -1:
            pos = video_url.find(",",prev_pos)
            if pos == -1:
                sub_url = video_url[prev_pos:]+"?rate=1500"
                prev_pos = -1
            else:
                sub_url = video_url[prev_pos:pos]+"?rate=1500"
                prev_pos = pos + 1
            urls.append(sub_url)
        if not urls:
            urls.append(video_url)
        filetype = url_helper.get_file_type(urls[0])
        return (urls,filetype)
    except:
        return (None,None)
        
