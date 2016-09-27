#!/bin/env python
# -*- coding: utf-8    -*- 
import os
import json

class AuditStaticsVideo(object):

    def __init__(self, userid=0, username="",  audit_success=0,  audit_fail=0, audit_total=0, ctime=""):
        self.uid = userid
        self.username = username
        self.audit_success = audit_success
        self.audit_fail = audit_fail
        self.audit_total = audit_success + audit_fail
        self.ctime = ctime
       

class AuditStaticsList(object):
    def __init__(self):
        self.userinfo_list = []
        self.uid_map = {}
        #self.audit_statics = None

    def  add_statics_info(self, uid, username, audit_success, audit_fail, audit_total, time):
        try:
            if not self.uid_map.has_key(uid):
                audit_statics = AuditStaticsVideo(uid, username, audit_success, audit_fail, audit_total, time)
                self.userinfo_list.append(audit_statics)
                self.uid_map[uid] = audit_statics
            return True
        except Exception,e:
            print e
            return False

    def add_success_num(self, uid):
        try:
            if self.uid_map.has_key(uid):
                statics_info = self.uid_map[uid]
                statics_info.audit_success += 1 
            return True
        except Exception,e:
            print e
            return False

    def add_fail_num(self, uid):
        try:
            if self.uid_map.has_key(uid):
                statics_info = self.uid_map[uid]
                statics_info.audit_fail += 1 
            return True
        except Exception,e:
            print e
            return False

    def to_infolist(self):
        list = []
        for index in range(len(self.userinfo_list)):
            item = self.userinfo_list[index]
            dict = {}
            #print item.uid, item.username, item.audit_success, item.audit_fail
            dict['uid'] = item.uid
            dict['username'] = item.username
            dict['success_num'] = item.audit_success
            dict['fail_num'] = item.audit_fail
            dict['total_num'] = item.audit_success + item.audit_fail
            dict['time'] = item.ctime
            list.append(dict)
        return list


