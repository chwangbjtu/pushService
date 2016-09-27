#!/home/admin/broker_project/build_tools/python272/bin/python
#-*- coding:utf-8 -*-

import platform

def unicode_to_local(unicode_str):
    if platform.system() == 'Windows': 
        return unicode_str.encode('gbk')
    else:
        return unicode_str

def local_to_unicode(local_str):
    if platform.system() == 'Windows': 
        return local_str.decode('gbk')
    else:
        return local_str

def utf8_to_local(utf8_str):
    if platform.system() == 'Windows': 
        return utf8_str.decode('utf-8').encode('gbk')
    else:
        return utf8_str

def local_to_utf8(local_str):
    if platform.system() == 'Windows': 
        return local_str.decode('gbk').encode('utf-8')
    else:
        return local_str

def ascii_to_local(ascii_str):
    if platform.system() == 'Windows': 
        return ascii_str.decode('ascii').encode('gbk')
    else:
        return ascii_str.decode('ascii').encode('utf-8')