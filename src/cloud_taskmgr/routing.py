#!/usr/bin/python
# -*- coding:utf-8 -*- 
import threading

class Router(object):
    """this is non thread-safe version"""
    __url_map = {}

    def __init__(self):
        pass

    def add(self,url,functor):
        if self.__url_map.has_key(url):
            return False
        self.__url_map[url] = functor
        return True

    def get_service_obj(self,url):
        if self.__url_map.has_key(url):
            return self.__url_map[url]
        return None
    
    def remove(self,url):
        if self.__url_map.has_key(url):
            del self.__url_map[url]
            return True
        return False

    def clear(self):
        __url_map = {}
