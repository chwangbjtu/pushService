#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

import json
import audit_mgr.audit_mgr
import audit_mgr.constant
import audit_mgr.audit_modify_info


@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def audit_video(request):
    try:
        mgr = audit_mgr.audit_mgr.AuditMgr.instance()
        result = request.POST["result"]
        tid = request.POST["tid"]
        funshion_id = request.POST["funshion_id"]
        ret,errinfo = (None,None)
        if result == "pass":
            modify_info = audit_mgr.audit_modify_info.AuditModifyInfo(title=request.POST["title"],logo=request.POST["logo"],
                                            channel=request.POST["channel"],tags=request.POST["tags"],
                                            description=request.POST["description"])
            ret,errinfo = mgr.audit_video(request.user.id,tid,funshion_id,1,modify_info)
        elif result == "deny":
            ret,errinfo = mgr.audit_video(request.user.id,tid,funshion_id,0)
        else:
            return render_to_response("error.html",{"error":"无效参数"})
        if ret == audit_mgr.constant.SUCCESS:
            return nav_to_next(request)
        args = {"href":"/audit/nextvideo/","title":"下一个视频"}
        return render_to_response("error.html",{"error":errinfo,"link":args})
    except Exception,e:
        return render_to_response("error.html",{"error":"缺少参数"})

@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def nav_to_next(request):
    try:
        mgr = audit_mgr.audit_mgr.AuditMgr.instance()
        #(code, num ,res) = mgr.get_pending_tasklist(request.user.id,1,1)
        (code, vinfo)=mgr.get_next_task(request.user.id)
        if code == audit_mgr.constant.SUCCESS:
            if not vinfo:
                args = {"error":"工作空间已经无待审核任务","link":{}}
                args["link"]["title"] = "继续申请任务"
                args["link"]["href"] = "/audit/applytask/"
                return render_to_response("error.html",args)

            import view_video
            return view_video.display_audit_video(vinfo,1)
    except Exception,e:
         pass
    return render_to_response("error.html",{"error":"内部错误"})

