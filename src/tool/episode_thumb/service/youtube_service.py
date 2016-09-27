# -*- coding: utf-8 -*-
import os
import urllib2
import traceback
import threading
from tornado import log
from http.http_client import HTTPClient
from db.episode_dao import EpisodeDao
from common.conf import Conf

class YoutubeDispatcher(threading.Thread):
    def __init__(self, site_id, thread_num = 4):
        threading.Thread.__init__(self)
        self._site_id = site_id
        self._thread_num = thread_num
        self._threads_nourl = []
        self._threads_undownload = []
        
    def run(self):
        self.check_directory()
        self.crawl_nourl_record()
        self.crawl_undownload_record()

    def check_directory(self):
        if not Conf.youtube_directory or os.path.exists(Conf.youtube_directory):
            return
        os.makedirs(Conf.youtube_directory, mode=0777)

    def crawl_nourl_record(self):
        log.app_log.debug("youtube dispather: crawl no url start...") 
        print "youtube dispather: crawl no url start..."
        crawl_type = 0
        result = self.get_episode_record(crawl_type)
        if result:
            N = self._thread_num
            for i in range(N):
                thread = YoutubeCrawler(result[((len(result)+N-1)/N)*i:((len(result)+N-1)/N)*(i+1)], crawl_type)
                self._threads_nourl.append(thread)
            for i in range(len(self._threads_nourl)):
                self._threads_nourl[i].start()
            for i in range(len(self._threads_nourl)):
                self._threads_nourl[i].join()
        log.app_log.debug("youtube dispather: crawl no url end...") 
        print "youtube dispather: crawl no url end..."

    def crawl_undownload_record(self):
        log.app_log.debug("youtube dispather: crawl undownload start...") 
        print "youtube dispather: crawl undownload start..."
        crawl_type = 1
        result = self.get_episode_record(crawl_type)
        if result:
            N = self._thread_num
            for i in range(N):
                thread = YoutubeCrawler(result[((len(result)+N-1)/N)*i:((len(result)+N-1)/N)*(i+1)], crawl_type)
                self._threads_undownload.append(thread)
            for i in range(len(self._threads_undownload)):
                self._threads_undownload[i].start()
            for i in range(len(self._threads_undownload)):
                self._threads_undownload[i].join()
        log.app_log.debug("youtube dispather: crawl undownload end...") 
        print "youtube dispather: crawl undownload end..."

    #def supermakedirs(self, path, mode):
    #    if not path or os.path.exists(path):
    #        return []
    #    (head, tail) = os.path.split(path)
    #    res = self.supermakedirs(head, mode)
    #    os.mkdir(path)
    #    os.chmod(path, mode)
    #    res = res + [path]
    #    return res

    def get_episode_record(self, has_img=0):
        episode_dao = EpisodeDao()
        if has_img == 0:
            res = episode_dao.get_nourl_record_by_site(self._site_id)
        else:
            res = episode_dao.get_undownload_record_by_site(self._site_id)
        episode_dao.close()
        return res

class YoutubeCrawler(threading.Thread):
    def __init__(self, record_list, has_img=0):
        threading.Thread.__init__(self)
        self._episode_dao = EpisodeDao()
        self._proxy_server = Conf.proxy_server
        self._http_client = HTTPClient(self._proxy_server)
        self._thumb_api = "http://img.youtube.com/vi/%s/hqdefault.jpg"
        self._record_list = record_list
        self._has_img = has_img

    def run(self):
        if self._http_client.check_opener() == True:
            self.crawl_thumb()
        self.close()

    def crawl_thumb(self):
        try:
            if self._has_img == 0:
                for record in self._record_list:
                    showid = record['show_id']
                    url = self._thumb_api % showid
                    code = []
                    response = self.get_data(url, code)
                    if code and code[0] == 404:
                        has_img = 3
                    else:
                        status = self.save_img(showid, response)
                        if status == True:
                            has_img = 2
                        else:
                            has_img = 1
                    self.update_thumb_status(showid, url, has_img)
            elif self._has_img == 1:
                for record in self._record_list:
                    showid = record['show_id']
                    url = record['thumb_url']
                    code = []
                    response = self.get_data(url, code)
                    if code and code[0] == 404:
                        has_img = 3
                    else:
                        status = self.save_img(showid, response)
                        if status == True:
                            has_img = 2
                        else:
                            has_img = 1
                    self.update_thumb_status(showid, url, has_img)
        except Exception, e:
            log.app_log.error("crawl thumb exception: %s" % traceback.format_exc())

    def get_data(self, url, code=[]):
        try:
            response = self._http_client.get_data(url, code)
            return response
        except Exception, e:
            log.app_log.error("get data exception: %s" % traceback.format_exc())
            log.app_log.debug("url:%s   proxy_server:%s" % (url, self._proxy_server))

    def save_img(self, showid, response):
        try:
            filename = showid + '.jpg'
            absolute_path = os.path.join(Conf.youtube_directory, filename)
            if not os.path.exists(absolute_path):
                if response:
                    content = response.read()
                    with open(absolute_path, 'wb') as fd:
                        fd.write(content)
                        return True
                return False
            return True
        except Exception, e:
            log.app_log.error("save image exception: %s" % traceback.format_exc())
            log.app_log.debug("image showid:%s" % showid)

    def update_thumb_status(self, showid, thumb_url, has_img):
        self._episode_dao.update_thumb_url(showid, thumb_url, has_img) 

    def close(self):
        if self._episode_dao:
            self._episode_dao.close()
