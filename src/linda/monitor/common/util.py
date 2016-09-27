# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import urllib2

class Util(object):

    @staticmethod
    def get_now_time(delta=0):
        now_time = datetime.now()
        if delta:
            now_time = Util.get_datetime_delta(now_time, delta)
        return now_time.strftime('%Y-%m-%d')

if __name__ == "__main__":
    print Util.get_now_time()
