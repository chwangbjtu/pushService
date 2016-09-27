# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import urllib2
import logging
import logging.handlers

class Util(object):

    RET_OK = 0
    RET_FAIL = 1
    RET_OK_BUSY = 2
    RET_FAIL_BUSY = 3
    RET_REJECT = 4
    RET_UNKNOWN = 5
    RET_DROP = 6
    RET_ERROR = 7

    SEND_STATUS = {'OK': 1, 'FAIL': 2, 'SENSITIVE': 3, 'REJECT': 4, 'DROP': 6, 'ERROR': 7}

    @staticmethod
    def init_logger():
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler("./log.txt", mode='a', maxBytes=1024*1024*10, backupCount=5)
        formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @staticmethod
    def get_datetime(s):
        format = '%Y-%m-%d %H:%M:%S'
        return datetime.strptime(s, format)

    @staticmethod
    def get_now_time(delta=0):
        now_time = datetime.now()
        if delta:
            now_time = Util.get_datetime_delta(now_time, delta)
        return now_time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_datetime_str(dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_datetime_delta(dt, minutes):
        return dt + timedelta(minutes=minutes)
    
    @staticmethod
    def get_delta_minutes(dt1, dt2):
        delta = dt1 - dt2
        return (delta.seconds + delta.days * 86400) / 60

    @staticmethod
    def get_vid(episode):
        if episode['site_name'] == 'sohu':
            return episode['url']
        elif episode['site_name'] == 'ifeng':
            s = episode['show_id']
            return '%s-%s-%s-%s-%s' % (s[:8], s[8:12], s[12:16], s[16:20], s[20:])
        else:
            return episode['show_id']

    @staticmethod
    def get_vid_from_url(site, url, show_id):
        if site == 'sohu':
            return url
        elif site == 'ifeng':
            s = show_id
            return '%s-%s-%s-%s-%s' % (s[:8], s[8:12], s[12:16], s[16:20], s[20:])
        elif site == 'youtube' or site == 'qy' or site == 'funshion' or site == 'k6':
            return url
        else:
            return show_id

    @staticmethod
    def unquote(text):
        return urllib2.unquote(text.encode('utf8')).decode('utf8')

if __name__ == "__main__":
    Util.init_logger()
    s = ['1970-01-01 00:00:00', '2014-06-05 14:35:47']
    d = Util.get_datetime(s[1]) - Util.get_datetime(s[0])
    print d.seconds + d.days * 86400
    print Util.get_now_time()
    print Util.get_now_time(delta=-20)
    print Util.get_datetime_str(Util.get_datetime(s[1]))
    print Util.get_datetime_delta(datetime.now(), -10)
    print Util.get_delta_minutes(Util.get_datetime(s[1]), Util.get_datetime(s[0]))

    s = ['%e8%ba%ab%e4%bb%bd%e8%af%81%2c%e7%81%ab%e6%9e%aa']
    print map(Util.unquote, s)
