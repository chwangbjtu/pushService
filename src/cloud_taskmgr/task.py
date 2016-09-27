#!/usr/bin/python
# -*- coding:utf-8 -*-

import exceptions

class Task(object):
    def __init__(self,cb_func = None):
        self._cb_func = cb_func
    
    def execute(self,args):
        raise exceptions.NotImplementedError()

    def pack_map_obj(self,args):
        raise exceptions.NotImplementedError()
