#!/usr/bin/python
# -*- coding:utf-8 -*-  
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
from urllib import urlencode

import time
import sys
import logging
import logging.handlers


if __name__ == "__main__":
    str1 = "http://192.168.16.113/video/2XNzkwMDU2NzQ4"
    url = urlencode(str(str1))
    print str
