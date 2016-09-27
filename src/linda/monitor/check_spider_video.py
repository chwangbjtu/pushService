# -*- coding:utf-8 -*-
from tornado import log
import traceback
import json

import sys
sys.path.append(".")
from common.conf import Conf
from common.util import Util

from db.episode_dao import EpisodeDao
from common.conv_json2html import generate_html
from common.sendmail import send_mail
from common.redis_mgr import RedisMgr

class Monitor(object):

    def __init__(self):
        self._ep_dao = EpisodeDao()
        self._since = '2016-4-1'
        self._redis_mgr = RedisMgr()

    def check_db(self):
        try:
            current_day = Util.get_now_time()
            channel = self._ep_dao.get_channel(self._since)

            res = {}
            for cn in channel:
                vc = self._ep_dao.get_video_count(cn, current_day)
                res[cn] = vc

            return res

        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def format_data(self, data):
        try:
            site = []
            for c, v in data.items():
                site += [item['site_name'] for item in v if item['site_name'] not in site]

            row = []
            for c, v in data.items():
                r = ['0'] * (len(site) + 2)
                r [0] = c
                total = 0
                for item in v:
                    site_index = site.index(item['site_name'])
                    r[site_index+1] = item['c']
                    total += item['c']
                r[-1] = total
                row.append(r)

            #last row
            lastr = ['总计']
            for i in range(1, len(site)+2):
                lastr.append(sum([int(r[i]) for r in row]))

            row.append(lastr)

            return ([u'频道'] + site + [u'总计'], row)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":

    try:
        ck = Monitor()
        data = ck.check_db()
        header, row = ck.format_data(data)
        stashed = ck._redis_mgr.get_count('mz_q')

        current_day = Util.get_now_time()
        table_data = {'title': u'爬虫视频每日统计', 'date': current_day, 'header': header, 'row': row, 'stashed': stashed}
        html_template = 'mail_template.html'
        cont = generate_html(table_data, html_template)

        send_mail(Conf.mail_host, Conf.mail_user, Conf.mail_passwd, Conf.mail_from, Conf.mail_to, Conf.mail_subject, cont)

    except Exception, e:
        log.app_log.error(traceback.format_exc())
