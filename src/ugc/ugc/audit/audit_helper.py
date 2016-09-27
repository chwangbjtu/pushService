#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import audit_video_info
import audit_mgr.audit_mgr
import audit_mgr.constant

def query_audit_info(tid):
    audit_info = audit_video_info.AuditVideoInfo()
    if not _query_base_info(tid,audit_info):
        return None
    funshion_info_list = _query_funshion_info(tid)
    if not funshion_info_list:
        return None
    for info in funshion_info_list:
        audit_info.funshion_list[info.rate] = info
    return audit_info

def _query_base_info(tid,baseinfo):
    try:
        mgr = audit_mgr.audit_mgr.AuditMgr.instance()
        ret,info = mgr.get_video_base(tid)
        if ret != audit_mgr.constant.SUCCESS:
            return False
        info = json.loads(info)
        baseinfo.tid = info['tid']
        baseinfo.site = info['site']
        baseinfo.title = info['title']
        baseinfo.tags = info['tags']
        baseinfo.origin = info['origin']
        baseinfo.channel = info['channel']
        baseinfo.description = info['description']
        baseinfo.priority = info['priority']
        baseinfo.step = info['step']
        baseinfo.status = info['status']
        baseinfo.video_id = info['video_id']
        baseinfo.seconds = info['seconds']
        baseinfo.ttype = info['ttype']
        baseinfo.user = info['username']
        #rint info['uid'], info['username'], info['tags'], info['title']
        return True
    except Exception,e:
        return False

def _query_funshion_info(tid):
    try:
        mgr = audit_mgr.audit_mgr.AuditMgr.instance()
        ret,infos = mgr.get_audit_task_details(tid)
        if ret != audit_mgr.constant.SUCCESS:
            return None
        funshion_list = []
        for item in infos:
            info_map = json.loads(item)
            funshion_item = audit_video_info.FunshionInfo()
            funshion_item.funshion_id = info_map['funshion_id']
            funshion_item.rate = info_map['rate']
            funshion_item.file_size = info_map['filesize']
            funshion_item.filename = info_map['filename']
            funshion_item.duration = info_map['duration']
            funshion_item.video_url = info_map['video_url']
            funshion_item.small_image = info_map['small_image']
            funshion_item.large_image = info_map['large_image']
            funshion_item.logo = info_map['logo']
            funshion_list.append(funshion_item)
        return funshion_list
    except Exception,e:
        return None


