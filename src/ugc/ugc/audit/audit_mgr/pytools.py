#!/bin/env python
# -*- coding: utf-8    -*-

debug = True
#debug = False
error = True

def get_func_name():
    import sys
    return sys._getframe(2).f_code.co_name

def show_value(data,data_name="test_value"):
    if debug: print 'debug: function: %s %s:%s' % (get_func_name(), data_name, data)

def show_str(content):
    if debug: print 'debug: function: %s content:%s' % (get_func_name(), content)

def show_error(content):
    if error: print 'error: function: %s content:%s' % (get_func_name(), content)
