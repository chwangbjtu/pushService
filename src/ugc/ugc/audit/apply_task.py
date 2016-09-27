#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

import audit_mgr.audit_mgr
import audit_mgr.constant
import audit_mgr.audit_modify_info

@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def apply_task(request):
    if request.method == "GET":
        site = ""
        if request.GET.has_key("site"):
            site = request.GET["site"]
        return render_to_response("apply_task.html",{"site":site})
    if request.method == "POST":
        args = {"error":"","link":{}}
        args["link"]["href"] = "/audit/applytask"
        args["link"]["title"] = "重新申请"

        try:
            count = int(request.POST["count"])
            title = request.POST["title"]
            channel = request.POST["channel"]
            site = request.POST["site"]
            fname = request.POST["fname"]
            start = request.POST["start"]
            end = request.POST["end"]
        except:
            args["error"] = "非法参数"
            return render_to_response("error.html",args)
        #apply task
        mgr = audit_mgr.audit_mgr.AuditMgr.instance()
        apply_info = audit_mgr.audit_modify_info.ApplyTaskInfo(request.user.id,count,site,channel,title,fname,start,end)
        ret,reason = mgr.apply_task(apply_info)
        if ret == audit_mgr.constant.SUCCESS:
            return render_to_response("apply_task_bk.html",{"count":int(reason)},)
        else:
            args["error"] = "申请失败"
            return render_to_response("error.html",args)
    else:
        return render_to_response("error.html",{"error":"invalid method"})
