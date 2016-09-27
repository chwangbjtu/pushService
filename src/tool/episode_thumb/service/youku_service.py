# -*- coding: utf-8 -*-
import os
import json
import traceback
import threading
from tornado import log
from http.http_client import HTTPClient
from db.episode_dao import EpisodeDao
from common.conf import Conf

class YoukuDispatcher(threading.Thread):
    def __init__(self, site_id, thread_num = 10):
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
        if not Conf.youku_directory or os.path.exists(Conf.youku_directory):
            return
        os.makedirs(Conf.youku_directory, mode=0777)

    def crawl_nourl_record(self):
        log.app_log.debug("youku dispather: crawl no url start...")
        print "youku dispather: crawl no url start..."
        crawl_type = 0
        result = self.get_episode_record(crawl_type)
        if result:
            N = self._thread_num
            for i in range(N):
                thread = YoukuCrawler(result[((len(result)+N-1)/N)*i:((len(result)+N-1)/N)*(i+1)], crawl_type)
                self._threads_nourl.append(thread)
            for i in range(len(self._threads_nourl)):
                self._threads_nourl[i].start()
            for i in range(len(self._threads_nourl)):
                self._threads_nourl[i].join()
        log.app_log.debug("youku dispather: crawl no url end...")
        print "youku dispather: crawl no url end..."

    def crawl_undownload_record(self):
        log.app_log.debug("youku dispather: crawl undownload start...")
        print "youku dispather: crawl undownload start..."
        crawl_type = 1
        result = self.get_episode_record(crawl_type)
        if result:
            N = self._thread_num
            for i in range(N):
                thread = YoukuCrawler(result[((len(result)+N-1)/N)*i:((len(result)+N-1)/N)*(i+1)], crawl_type)
                self._threads_undownload.append(thread)
            for i in range(len(self._threads_undownload)):
                self._threads_undownload[i].start()
            for i in range(len(self._threads_undownload)):
                self._threads_undownload[i].join()
        log.app_log.debug("youku dispather: crawl undownload end...")
        print "youku dispather: crawl undownload end..."

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

class YoukuCrawler(threading.Thread):
    def __init__(self, record_list, has_img=0):
        threading.Thread.__init__(self)
        self._episode_dao = EpisodeDao()
        self._proxy_server = None
        self._http_client = HTTPClient(self._proxy_server)
        self._thumb_api = "http://v.youku.com/player/getPlayList/VideoIDS/%s" 
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
                    response = self.get_data(url)
                    img_url = self.parse_data(response)
                    if img_url:
                        code = []
                        response = self.get_data(img_url, code)
                        if code and code[0] == 404:
                            has_img = 3         # server not found
                        else:
                            status = self.save_img(showid, response)
                            if status == True:
                                has_img = 2     # download successfully
                            else:
                                has_img = 1     # download failed
                    else:
                        has_img = 0             # parse failed, need to reparse
                    self.update_thumb_status(showid, img_url, has_img)
            elif self._has_img == 1:
                for record in self._record_list:
                    showid = record['show_id']
                    img_url = record['thumb_url']
                    if img_url:
                        code = []
                        response = self.get_data(img_url, code)
                        if code and code[0] == 404:
                            has_img = 3
                        else:
                            status = self.save_img(showid, response)
                            if status == True:
                                has_img = 2
                            else:
                                has_img = 1
                    else:
                        has_img = 0
                    self.update_thumb_status(showid, img_url, has_img)
        except Exception, e:
            log.app_log.error("crawl thumb exception: %s" % traceback.format_exc())

    def get_data(self, url, code=[]):
        try:
            response = self._http_client.get_data(url, code)
            return response
        except Exception, e:
            log.app_log.error("get data exception: %s" % traceback.format_exc())
            log.app_log.debug("url:%s   proxy_server:%s" % (url, self._proxy_server))

    def parse_data(self, response):
        try:
            if response:
                # first time: content is json
                content = response.read()
                content = json.loads(content)
                if content:
                    content = content["data"]
                    if content:
                        content = content[0]
                        if content:
                            content = content["logo"]
                            return content
                # it does not need
                #if response.info().get('Content-Encoding') == 'gzip':
                #    content = self.ungzip(content)
                #if response.info().get('Conent-Encoding') == 'deflate'
                #    content = self.undeflate(content)
        except Exception, e:
            log.app_log.error("parse data exception : %s", traceback.format_exc())

    def save_img(self, showid, response):
        try:
            filename = showid + '.jpg'
            absolute_path = os.path.join(Conf.youku_directory, filename)
            if not os.path.exists(absolute_path):
                if response:
                    content = response.read()
                    with open(absolute_path,'wb') as fd:
                        fd.write(content)
                    return True
                return False
            return True
        except Exception, e:
            log.app_log.error("save image exception: %s" % traceback.format_exc())
            log.app_log.debug("image showid:%s" % showid)

    def update_thumb_status(self, showid, thumb_url, has_img):
        if self._episode_dao:
            self._episode_dao.update_thumb_url(showid, thumb_url, has_img) 

    def close(self):
        if self._episode_dao:
            self._episode_dao.close()

    #def ungzip(self, data):
    #    try:
    #        compressed_stream = StringIO.StringIO(data)
    #        gzipper = gzip.GzipFile(fileobj=compressed_stream)
    #        return gzipper.read()
    #    except Exception, e:
    #        log.app_log.error("ungzip data exception: %s " % traceback.format_exc())
    #        log.app_log.debug("data: %s" % data)

    #def undeflate(self, data):
    #    try:
    #        #implement
    #        return data
    #    except Exception, e:
    #        log.app_log.error("undeflate data exception: %s " % traceback.format_exc())
    #        log.app_log.debug("data: %s" % data)
