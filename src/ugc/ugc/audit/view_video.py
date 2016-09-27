#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings


class AuditVideoArgs(object):
    def __init__(self):
        self.tid = ""
        self.funshion_id = ""
        self.title = ""
        self.tags = ""
        self.channel = ""
        self.description = ""
        self.small_image_list = []
        self.image_logo = ""
        self.large_image = ""
        self.duration = ""
        self.user = ""
        self.ttype = None
        self.video_url = ""
        self.page_views = ""
        self.audit_state = ""
        self.audit_code = None


def parse_to_args(vinfo):
    arg = AuditVideoArgs()
    arg.tid = vinfo.tid
    arg.title = vinfo.title
    arg.tags = vinfo.tags
    arg.channel = vinfo.channel
    if vinfo.channel:
        pos = vinfo.channel.rfind("频道")
        if pos != -1:
            arg.channel = vinfo.channel[:pos]
    arg.description = vinfo.description
    arg.user = vinfo.user
    arg.ttype = vinfo.ttype
    if vinfo.step == "audit":
        arg.audit_code = vinfo.status
    else:
        arg.audit_code = 1
    state_text = ("待审核","审核通过","审核不通过")
    arg.audit_state = state_text[arg.audit_code]
    #funshion info
    if not vinfo.funshion_list:
        return None
    key = vinfo.funshion_list.keys()[0]
    funshion_info = vinfo.funshion_list[key]
    #large image
    arg.large_image = funshion_info.large_image
    #small image
    img_list = funshion_info.small_image.split("|")
    for item in img_list:
        item = item.strip()
        if item :
            arg.small_image_list.append(item)
    arg.image_logo = funshion_info.logo
    #video url
    arg.video_url = funshion_info.video_url
    #duration
    seconds = funshion_info.duration/1000
    hours = seconds/3600
    minu = (seconds - hours*3600)/60
    seconds = seconds - hours*3600 - minu*60
    arg.duration = "%d:%d:%d" % (hours,minu,seconds)
    #funshion id
    arg.funshion_id = funshion_info.funshion_id
    return arg

def display_audit_video(vinfo,edit):
    arg = parse_to_args(vinfo)
    if not arg:
        return render_to_response("error.html","参数错误")
    if edit == 1 and arg.audit_code != 0:
        edit = 0
    #channels = ("旅游","科技","汽车","游戏","生活","搞笑","时尚")
    channels = (
                "美女",
                "搞笑",
                "娱乐",
                "游戏",
                "体育",
                "汽车",
                "科技",  
                "军事",
                "音乐",
                "生活",
                "时尚",
                "旅游",
                "母婴",
                "健康",
                "公开课",
                "纪录片",
                "广告",
                "微电影",
                "广场舞",
                "生活百科",
                "youtube精选",
                "电影片花",
                "电视片花",
                "综艺片花",
                "动漫片花",
                "片花",
                "其他")
    if not arg.channel in channels:
        arg.channel = channels[-1]
    return render_to_response("audit_video.html",{"vinfo":arg,"channel_list":channels,"edit":edit})

