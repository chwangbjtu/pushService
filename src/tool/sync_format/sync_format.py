# -*- coding:utf-8 -*-
import urllib2
import traceback
import time
import logging
import json
from db_connect import MysqlConnect
from episode_dao import EpisodeDao
from http_client import HttpClient
from util import Util

class SyncServer(object):

    def __init__(self):
        self._db_conn = MysqlConnect()
        self._ep_dao = EpisodeDao(self._db_conn)
        self._http_client = HttpClient()
        self._flvcd_url = 'http://vpwind.flvcd.com/parse-fun.php'

    def commit_transaction(self):
        self._db_conn.commit()

    def request_format(self, url):
        try:
            dest_url = self._flvcd_url + '?url=%s' % urllib2.quote(url)
            ret = self._http_client.get_data(dest_url)
            if ret[0] == 200:
                ret_json = json.loads(ret[1])
                if 'formatCodeList' in ret_json and ret_json['formatCodeList']:
                    format_list = ret_json['formatCodeList'].split('|')
                    return format_list[-1]
        except Exception, e:
            logging.error(traceback.format_exc())

    def start(self):
        while True:
            try:
                since = -43200#miniutes
                since_time = Util.get_now_time(delta=since)
                episode = self._ep_dao.get_low_episode_since(since_time)

                for ep in episode:
                    logging.info(json.dumps(ep))
                    format = self.request_format(ep['url'])
                    if format:
                        episode = self._ep_dao.update_format(ep['id'], format)

            except Exception, e:
                logging.error(traceback.format_exc())

            time.sleep(60)

def test():
    sync_server = SyncServer()
    Util.init_logger()
    print sync_server.request_format('http://www.iqiyi.com/v_19rro4ljrk.html')

if __name__ == "__main__":

    Util.init_logger()
    sync_server = SyncServer()
    sync_server.start()
