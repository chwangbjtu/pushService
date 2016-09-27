#!/usr/bin/python
# -*- coding:utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from db.repost_datas import RepDatas 
from plat.settings import FLASHGET_SERVER_IP, FLASHGET_SERVER_PORT, FLASHGET_GET_URL, UPLOAD_SERVER_IP, UPLOAD_SERVER_PORT
import httplib
import math
import json
from subscribe.models import *
from subscribe.pager import Pager
from api.parse import do_parse
import logging
logger = logging.getLogger('my')

classifi_ITEM = [['娱乐',u'娱乐'],['体育',u'体育'],['新闻',u'新闻'],['搞笑',u'搞笑'],\
                     ['汽车',u'汽车'],['母婴',u'母婴'],['旅游',u'旅游'],['时尚',u'时尚'],['健康',u'健康'],\
                     ['科技',u'科技'],['游戏',u'游戏'],['美女',u'美女'],['电视片花',u'电视片花'],\
                     ['电影片花',u'电影片花'],['综艺片花',u'综艺片花'],['动漫片花',u'动漫片花'],['纪录片',u'纪录片'],\
                     ['热点',u'热点'],['公开课',u'公开课'],['财经',u'财经'],['音乐',u'音乐'],['军事',u'军事'],\
                     ['广场舞',u'广场舞'],['梦之声',u'梦之声'],['生活百科',u'生活百科'],['微电影',u'微电影']]
step_id_rep = {'0':u'初始','10':u'下载','20':u'发送','30':u'提交','40':u'转码','50':u'审核','60':u'打包','70':u'分发'}
status_rep = {'0': u'中','1': u'成功', '2': u'失败', '3': u'敏感', '4': u'被拒绝', '6': u'被丢弃', '7': u'内部出错'}

def get_task_representation(step, status):
    step = str(step)
    status = str(status)

    part1 = step_id_rep[step] if step in step_id_rep else ''
    part2 = status_rep[status] if status in status_rep else ''
    return part1 + part2

@csrf_exempt
@login_required
def repost(request):  
    tips = " "
    if request.method == 'POST':
        username = request.user.username
        uid = request.user.id
        
        show_id = request.POST.get("show_id", "")
        site_name = request.POST.get("site", "")
        url = request.POST.get("url", "")
        title = request.POST.get("title", "")
        tags = request.POST.get("tags", "")
        desc = request.POST.get("desc", "")
        priority = request.POST.get("priority", "")
        channel = request.POST.get("channel", "")

        inst = RepDatas.instance()
        site_list = inst.get_site_list()
        site_id = [s['site_id'] for s in site_list if s['site_name'] == site_name]
        ret = inst.add_repost(uid, show_id, url, title, tags, desc, priority, channel, site_id[0])
        logger.info(u"%s 添加普通转帖, url:%s",username,url)
        tips = "转帖成功" if ret else "转帖失败"

    classifi_item = classifi_ITEM  
    return render_to_response('repost.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def repost_space(request):
    username = request.user.username
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    
    inst = RepDatas.instance()
    video_list = inst.get_repost_video(username, page, count)
    #print video_list
    video_total = int(inst.get_repost_video_count(username))  
    
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    for v in video_list:
        v['result'] = get_task_representation(v['step_id'], v['status'])
        if not v['result']:
            v['result']=u'未处理'
      
    return render_to_response('repost_space.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def batch_repost(request):  
    if request.method == 'POST':
        username = request.user.username
        uid = request.user.id

        links = request.POST.get('links')
        priority = request.POST.get('priority')
        channel = request.POST.get('channel')

        result = {'ok': [], 'fail':[]}
        if links:
            logger.info(u"%s 添加批量转帖", username)
            url = links.split('\r\n')
            inst = RepDatas.instance()
            site_list = inst.get_site_list()
            for u in url:
                if not u:
                    continue
                res = do_parse(u)

                if str(res['ret']) == '0' and res['show_id'] and res['title']:
                    site_id = [s['site_id'] for s in site_list if s['site_name'] == res['site']]
                    ret = inst.add_repost(uid, res['show_id'], u, res['title'], res['tag'], res['description'], priority, channel, site_id[0])
                    if ret:
                        result['ok'].append(u)
                    else:
                        result['fail'].append(u)
                else:
                    result['fail'].append(u)

    classifi_item = classifi_ITEM  
    return render_to_response('batch_repost_result.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def upload_content(request):
    username = request.user.username
    uid = request.user.id
    uploader_domain = 'http://' + UPLOAD_SERVER_IP + ':' + UPLOAD_SERVER_PORT

    if request.method == 'POST':
        try:
            show_id = request.POST.get("show_id", "")
            title = request.POST.get("title", "")
            tags = request.POST.get("tags", "")
            desc = request.POST.get("desc", "")
            priority = request.POST.get("priority", "")
            channel = request.POST.get("channel", "")
            audit = request.POST.get("audit_free", "")

            #get url from flashget
            try:
                conn = httplib.HTTPConnection(FLASHGET_SERVER_IP, FLASHGET_SERVER_PORT)
                body = {'taskid': show_id}
                conn.request('POST', FLASHGET_GET_URL, json.dumps(body))
                response = conn.getresponse()
                ret_json = json.loads(response.read())
                if str(ret_json['ret']) == '0':
                    url = ret_json['url']
                    RepDatas.instance().add_upload_content(uid, show_id, title, tags, desc, priority, channel, audit, url)
                    ret, msg  = ('0', u'上传成功')
                else:
                    ret, msg  = ('1', u'flashget return fail')
            except Exception, e:
                logger.error(e)
                ret, msg  = ('1', str(e))

        except Exception, e:
            logger.error(e)
            ret, msg  = ('1', str(e))
        logger.info(u"%s 上传%s, 标题:%s", username, show_id, title)
        return StreamingHttpResponse(json.dumps({'ret': ret, 'msg': msg}))

    classifi_item = classifi_ITEM  
    return render_to_response('upload.html', locals(), context_instance=RequestContext(request))
    
