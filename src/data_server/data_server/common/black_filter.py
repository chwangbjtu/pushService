# -*- coding:utf-8 -*-
"""class for manage black worlds"""
import re
import time
import traceback
from tornado import log
#from conf import Conf
import sys
sys.path.append('.')
from db.db_connect import MysqlConnect
from db.blacklist_dao import BlacklistDao 
import threading

class RWLock(object):
    def __init__(self):
        self._rlock = threading.Lock();
        self._wlock = threading.Lock();
        self._reader = 0

    def write_acquire(self):
        self._wlock.acquire()

    def write_release(self):
        self._wlock.release()

    def read_acquire(self):
        self._rlock.acquire()
        self._reader += 1
        if self._reader == 1:
            self._wlock.acquire()
        self._rlock.release()

    def read_release(self):
        self._rlock.acquire()
        self._reader -= 1
        if self._reader == 0:
            self._wlock.release()
        self._rlock.release()

class BlackFilter(object):
 
    @classmethod
    def get_ins(cls):
        if not hasattr(cls, "_ins"):
            cls._ins = cls()
        return cls._ins

    def __init__(self):
        self._black_set = set()
        self._ignor = u'[\s|\u2600-\u26ff]*'
        self._rwlock = RWLock()

    def reload_blacklist(self):
        try:
            log.app_log.debug("blacklist has changed, reload blacklist")
            return self.load_blacklist()
        except Exception, e:
            log.app_log.error("reload blacklist error: %s" % e)

    
    #load blacklist from database
    def load_blacklist(self):
        try:
            db_conn = MysqlConnect()
            if db_conn:
                blacklist_dao = BlacklistDao(db_conn) 
                res = blacklist_dao.get_blacklist_words()
                #加锁
                self._rwlock.write_acquire()
                if self._black_set:
                    self._black_set.clear()
                for item in res:
                    for key in item.keys():
                        word = item[key]
                        pattern = self._ignor.join([re.escape(w) for w in list(word)])
                        self._black_set.add(re.compile(pattern))
                #释放锁
                self._rwlock.write_release()
                db_conn.close()
                return len(self._black_set)
            else:
                return None
        except Exception, e:
            self._rwlock.write_release()
            log.app_log.error("load blacklist error: %s" % e)

    def add_black_word(self, word):
        try:
            #log.app_log.debug('add: %s, %s, %s' % (word, repr(word), type(word)))
            self._rwlock.write_acquire()
            pattern = self._ignor.join([re.escape(w) for w in list(word)])
            self._black_set.add(re.compile(pattern))
            self._rwlock.write_release()
            return True
        except Exception, e:
            self._rwlock.write_release()
            log.app_log.error("add black word error: %s" % e)
            return False

    def filt_word(self, keyword):
        try:
            if not isinstance(keyword, unicode):
                if isinstance(keyword, str):
                    keyword = unicode(keyword.decode('utf8'))
                else:
                    keyword = unicode(keyword)
            #log.app_log.debug('filt: %s, %s, %s' % (keyword, repr(keyword), type(keyword)))
            result = False
            #加锁
            self._rwlock.read_acquire()
            for p in self._black_set:
                mgroup = p.search(keyword)
                if mgroup:
                    log.app_log.debug('sensitive: %s' % keyword)
                    result = True
                    break
            #释放锁
            self._rwlock.read_release()
            return result
        except Exception, e:
            self._rwlock.read_release()
            log.app_log.error("fail to filt word [%s]: %s" % (keyword, traceback.format_exc()))

if __name__ == "__main__":

    fbw = BlackFilter.get_ins()
    c = fbw.load_blacklist()
    log.app_log.debug('keyword black list count: %s' % c)
    fbw.filt_word(u'高仿人名币直销，快来买')
    fbw.filt_word(u'高\u2605仿')
    fbw.filt_word(u'人\u2605民\u2605币')
    fbw.filt_word(u'直\u2605销')
    fbw.filt_word(u'高仿人民币直销，快来买')
    fbw.filt_word(u'出售高\u2605仿\u2604人民币直\u2606销，快来买')
    fbw.filt_word(u'出售高 仿 人 民 币直 \u2607 销，快来买')
    fbw.filt_word(u'')
    fbw.filt_word(u'\u65f6\u5c1a\u9891\u9053|\u65f6\u5c1a\u5217\u8868|\u670d\u88c5\u670d\u9970')
    fbw.filt_word('2014-06-12 18:36:03')
    fbw.filt_word(u'\u89c6\u9891: \u6743\u76f8\u4f51\u5d14\u667a\u53cb2004\u5e74\u4e0a\u6d77\u5b89\u5fb7\u70c8\u91d1\u65f6\u88c5\u79c0')
    fbw.filt_word('XNzI1MTc5NTQw')
    fbw.filt_word(480)
    fbw.filt_word(u'\u6743\u76f8\u4f51|\u5d14\u667a\u53cb|\u5929\u56fd\u7684\u9636\u68af')
    fbw.filt_word(u'办')
    fbw.filt_word(u'制作')
    fbw.filt_word(u'宝宝')
    fbw.filt_word(u'母婴')
    fbw.filt_word(u'开车')
    fbw.filt_word(u'开度')
    fbw.filt_word(u'zJGC4aGfGoQ')
    fbw.filt_word(u'斯巴鲁WRX STI跑马场  VS  本田CRF450R')
    fbw.filt_word(u'黑名单')
    fbw.filt_word(u'测试一个')
