#!/bin/env python
# -*- coding: utf-8    -*- 

#审核修改信息结构体
class AuditModifyInfo(object):  
    def __init__(self, title="", channel="", tags="", description="", logo="", ttype=0):
        self.title = title
        self.channel = channel
        self.tags = tags
        self.description = description
        self.logo = logo
        self.ttype = ttype


#申请任务修改信息结构体
class ApplyTaskInfo(object):  
    def __init__(self, uid=1, apply_num = 1, site="", channel="", title="",  f_username = "", begin_time="", end_time=""):
        self.uid = uid
        self.apply_num = apply_num
        self.site = site
        self.channel = channel
        self.title = title
        self.f_username = f_username
        self.begin_time = begin_time
        self.end_time = end_time
        

