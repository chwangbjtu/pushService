#!/usr/bin/python
# -*- coding:utf-8 -*-  

import time
import sys
import etc
import http_server

def main():
    
    server = http_server.HttpServer()
    server.start(etc.SERVICE_PORT)
    
    while True:
        time.sleep(86400)

if __name__ == "__main__":
    main()
