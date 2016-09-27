# -*- coding:utf-8 -*-
"""class for manage black worlds"""
import re
import time
import traceback

import sys
sys.path.append('.')

class BlackChecker(object):
 
    @classmethod
    def get_ins(cls):
        if not hasattr(cls, "_ins"):
            cls._ins = cls()
        return cls._ins

    def __init__(self):
        self._keyword_set = set()
        self._black_set = set()

    def load_black_word(self, black_file):
        try:
            fd = open(black_file, 'r')
            for line in fd:
                kw = line.strip()
                if kw:
                    self._keyword_set.add(kw)
                self._black_set.add(kw)
            fd.close()
            return (len(self._keyword_set), len(self._black_set))
        except IOError, e:
            print 'read black list [%s] error: %s' % (black_file, e)

    def resave_black(self, black_file):
        try:
            fd = open(black_file, 'w')
            for b in self._black_set:
                fd.write('%s\n' % b)
            fd.close()
        except IOError, e:
            print 'read black list [%s] error: %s' % (black_file, e)

    def check_black(self):
        try:
            count = len(self._keyword_set)
            index = 1
            for k in self._keyword_set:
                print 'progress: %s%%\r' % str(index * 100 / count),;
                pattern = re.compile(re.escape(k), re.I)
                duplicate_black = []
                for b in self._black_set:
                    if b != k:
                        mgroup = pattern.search(b)
                        if mgroup:
                            duplicate_black.append(b)
                #print '%s: %s' % (k, "|".join(duplicate_black))
                self._black_set = self._black_set.difference(set(duplicate_black))
                index += 1
        except Exception, e:
            print "fail to check: %s" % e

if __name__ == "__main__":

    fbw = BlackChecker.get_ins()
    c = fbw.load_black_word('black.utf8.txt')
    print 'keyword black list count: %s %s' % (c[0], c[1])
    fbw.check_black()
    fbw.resave_black('t.txt')
