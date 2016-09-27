#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from ugc.db.db_mgr import DbManager
from ugc.show.pager import Pager
import math

step_rep = {'audit': u'审核', 'transcode': u'转码', 'mpacker': u'打包', 'distribute': u'分发'}
status_rep = {'0': u'未', '1': u'成功', '2': u'失败'}

def get_task_representation(step, status):
    step = str(step)
    status = str(status)

    part1 = step_rep[step] if step in step_rep else ''
    part2 = status_rep[status] if status in status_rep else ''

    if part1 == '' or part2 == '':
        return step + status
    if str(status) ==  '0':
        return part2 + part1
    return part1 + part2

@login_required
@permission_required("ugc.can_show_audit",login_url="/forbidden/")
def show_video(request):
    origin = request.GET.get('origin', 'all')
    status = request.GET.get('status', 'all')
    sort = request.GET.get('sort', 'ctime')

    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))

    status_filter = [["all", u"全部"], ["unaudit", u"待审"], ["pass", u"已通过"], ["unpass", u"未通过"], ["untrans", u"待转码"], ["fail", u"失败"]]
    origin_filter = [["all", u"全部"], ["upload", u"上传"], ["forwards", u"转帖"], ["youku", u"YK爬虫"], ["youtube", u"YT爬虫"]]
    sort_filter = [["pub_time", u"按发布时间"], ["ctime", u"按创建时间"], ["mtime", u"按修改时间"], ["priority", u"按优先级"]]

    mgr = DbManager.instance()
    video_list = mgr.get_video(page, count, origin, status, sort)
    video_total = int(mgr.get_video_count(origin, status))

    #get video status
    for v in video_list:
        v['result'] = get_task_representation(v['step'], v['status'])

    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)

    return render_to_response("show_video.html", {'video_list': video_list, 'page': page, 'count': count, 'page_list': pg.get_page_items(), 'page_count': page_count, 'total': video_total, 'origin': origin, 'status': status, 'sort': sort, 'status_filter': status_filter, 'origin_filter': origin_filter, 'sort_filter': sort_filter})

@login_required
@permission_required("ugc.can_show_audit",login_url="/forbidden/")
def show_unaudit(request):
    if request.method == 'POST':
        tid = request.POST.getlist('sel', [])
        if tid:
            uid = request.user.id
            mgr  = DbManager.instance()
            mgr.apply_task(uid, tid)

    origin = request.GET.get('origin', 'all')
    sort = request.GET.get('sort', 'ctime')

    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))

    origin_filter = [["all", u"全部"], ["upload", u"上传"], ["forwards", u"转帖"], ["youku", u"YK爬虫"], ["youtube", u"YT爬虫"]]
    sort_filter = [["pub_time", u"按发布时间"], ["ctime", u"按创建时间"], ["mtime", u"按修改时间"], ["priority", u"按优先级"]]

    mgr  = DbManager.instance()
    video_list = mgr.get_video(page, count, origin, "unaudit", sort)
    video_total = int(mgr.get_video_count(origin, "unaudit"))
    audit_task = mgr.get_all_task()

    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)

    return render_to_response("show_unaudit.html", {'video_list': video_list, 'audit_task': audit_task, 'page': page, 'count': count, 'page_list': pg.get_page_items(), 'page_count': page_count, 'total': video_total, 'origin': origin, 'sort': sort, 'origin_filter': origin_filter, 'sort_filter': sort_filter})


if __name__ == "__main__":
    step = ['audit', 'transcode', 'mpacker', 'distribute']
    status = [0, 1, 2]
    for s in step:
        for t in status:
            res = get_task_representation(s, t)
            print '[%s %s] [%s]' % (s, t, res)
            

