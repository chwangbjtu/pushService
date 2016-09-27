#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required

import audit_video_info
import view_video
import audit_helper

@login_required
def show_task(request):
    if not request.GET.has_key("tid"):
        return render_to_response("error.html",{"error":"缺乏参数"})
    tid = request.GET["tid"]
    vinfo = audit_helper.query_audit_info(tid)
    if not vinfo:
        return render_to_response("error.html",{"error":"获取视频信息失败"})
    edit = 1
    if request.GET.has_key("edit") and request.GET["edit"] == "0":
        edit = 0
    return view_video.display_audit_video(vinfo,edit)