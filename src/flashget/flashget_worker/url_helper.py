#!/usr/bin/python
# -*- coding:utf-8 -*-

def get_urlfile_ext(url_str):
    pos = url_str.find("?")
    if pos != -1:
        start = url_str.rfind(".",0,pos)
        if start != -1:
            return url_str[start:pos]
    else:
        start = url_str.rfind(".")
        if start != -1:
            return url_str[start:]
    return None
    
def get_file_type(url_str):
    ext = get_urlfile_ext(url_str)
    if ext == ".f4v" or ext == ".flv":
        return "flv"
    if ext == ".mp4":
        return "mp4"
    return "unknown"
