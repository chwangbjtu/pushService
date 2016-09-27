# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

class Util(object):

    RET_OK = 0
    RET_FAIL = 1
    RET_OK_BUSY = 2
    RET_FAIL_BUSY = 3
    RET_REJECT = 4
    RET_UNKNOWN = 5

    @staticmethod
    def get_datetime(s):
        format = '%Y-%m-%d %H:%M:%S'
        return datetime.strptime(s, format)

    @staticmethod
    def get_now_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_datetime_str(dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_datetime_delta(dt, minutes):
        return dt - timedelta(minutes=minutes)
    
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

if __name__ == "__main__":
    s = ['1970-01-01 00:00:00', '2014-06-05 14:35:47']
    d = Util.get_datetime(s[1]) - Util.get_datetime(s[0])
    print d.seconds + d.days * 86400
    print Util.get_now_time()
    print Util.get_datetime_str(Util.get_datetime(s[1]))
    print Util.get_datetime_delta(datetime.now(), 10)
    print Util.get_delta_minutes(Util.get_datetime(s[1]), Util.get_datetime(s[0]))
