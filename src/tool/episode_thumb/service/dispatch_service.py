# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
import traceback
from tornado import log
from db.site_dao import SiteDao
from youku_service import YoukuDispatcher
from youtube_service import YoutubeDispatcher

class CrawlerDispatcher(object):
    def __init__(self):
        self._threads = []
        self._thread_num_youku = 16
        self._thread_num_youtube = 4
    
    def start(self):
        self._site_list = self.get_sites()
        # ku6, iqiyi, ifeng etc do not work
        #self._thread_num = len(self._site_list)
        self.dispatcher()
        

    def get_sites(self):
        site_dao = SiteDao()   
        res = site_dao.get_sites() 
        site_dao.close()
        return res

    def dispatcher(self):
        try:
            for site in self._site_list:
                if site:
                    site_name = site['site_name']
                    site_id = site['site_id']
                    self.create_thread(site_name, site_id)
            for t in self._threads:
                t.start()
            for t in self._threads:
                t.join()
        except Exception, e:
            log.app_log.error("dispatcher exception: %s" % traceback.format_exc())
            
    def create_thread(self, site_name, _site_id):
        if site_name == "youku":
            #pass
            thread = YoukuDispatcher(site_id=_site_id, thread_num=self._thread_num_youku)
            self._threads.append(thread)
        elif site_name == "youtube":
            #pass
            thread = YoutubeDispatcher(site_id=_site_id, thread_num=self._thread_num_youtube)
            self._threads.append(thread)
            
        #elif site_name == "sohu":
        #elif site_name == "ifeng":
        #elif site_name == "iqiyi":
        #elif site_name == "ku6":
        #elif site_name == "funshion":
