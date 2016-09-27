#-*- coding: utf-8 -*-
import traceback
import urllib2
import time
from tornado import log

class HTTPClient(object):
    def __init__(self, proxy_server=None):
        self._timeout = 5
        self._proxy_server = proxy_server
        self._opener = None
        self.build_opener()

    def build_opener(self):
        try:
            opener = None
            if self._proxy_server:
                proxy_handler = urllib2.ProxyHandler({"http" : r'http://%s' % self._proxy_server})
                # need username and password
                #proxy_handler = urllib2.proxyHandler({"http": r"http://user:password@192.168.160.100:8088"})
                if proxy_handler:
                    opener = urllib2.build_opener(proxy_handler)
            else:
                opener = urllib2.build_opener()
            if opener:
                opener.addheaders = [{'User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}]
            self._opener = opener
        except Exception, e:
            log.app_log.error("set opener exception: %s" % traceback.format_exc())

    def check_opener(self):
        if self._opener:
            return True
        log.app_log.debug("urllib2 opener is unavailable...")
        return False

    def get_data(self, url, code=[]):
            if self._opener:
                try:
                    time.sleep(2)
                    response = self._opener.open(url)
                    return response
                except urllib2.HTTPError, he:
                    code.append(he.code)
                    log.app_log.error("get data exception: %s" % traceback.format_exc())
                    log.app_log.debug("url:%s" % url)
                except urllib2.URLError, ue:
                    try:
                        time.sleep(5)
                        log.app_log.debug("url:%s   try again" % url)
                        response = self._opener.open(url)
                        if response:
                            log.app_log.debug("url:%s try again successfully." % url)
                            return response
                        else:
                            log.app_log.debug("url:%s try again failed" % url)
                    except Exception, e:
                        log.app_log.error("get data exception: %s" % traceback.format_exc())
                        log.app_log.debug("url:%s" % url)
                except Exception, e:
                    log.app_log.error("get data exception: %s" % traceback.format_exc())
                    log.app_log.debug("url:%s" % url)
