# -*-coding:utf-8 -*-
from singleton import Singleton

class Statistics(Singleton):        
    def init_data(self, total, msgid, pull_id):
        self._data = {}
        self._data['pull_id'] = pull_id
        self._data['total'] = total
        self._data['msgid'] = msgid
        self._data['fail'] = 0
    
    def add_failed_num(self):
        self._data['fail'] += 1
        
    def get_result(self):
        self._data['success'] = self._data['total'] - self._data['fail']
        return self._data
        