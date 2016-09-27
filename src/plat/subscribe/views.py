#!/usr/bin/python
# -*- coding:utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from models import *
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import re
from django.db import connection
from itertools import chain
from db.ugc_video_dao import UgcVideoDao
import math
from pager import Pager
import urllib2
import json
import os
import logging
from plat.settings import SCRAPYD_COMMAND
logger = logging.getLogger('my')

order_ITEM = [['',u'排序方式'],['1',u'播放数'],['2',u'订阅数']]
status_ITEM = [['',u'所有状态'],['1',u'已订阅'],['2',u'未订阅']]
classifi_ITEM = [['',u'所有分类'],['娱乐',u'娱乐'],['体育',u'体育'],['新闻',u'新闻'],['搞笑',u'搞笑'],\
                     ['汽车',u'汽车'],['母婴',u'母婴'],['旅游',u'旅游'],['时尚',u'时尚'],['健康',u'健康'],\
                     ['科技',u'科技'],['游戏',u'游戏'],['美女',u'美女'],['电视片花',u'电视片花'],\
                     ['电影片花',u'电影片花'],['综艺片花',u'综艺片花'],['动漫片花',u'动漫片花'],['纪录片',u'纪录片'],\
                     ['热点',u'热点'],['公开课',u'公开课'],['财经',u'财经'],['音乐',u'音乐'],['军事',u'军事'],\
                     ['广场舞',u'广场舞'],['梦之声',u'梦之声'],['生活百科',u'生活百科'],['微电影',u'微电影']]
#     classifi_ITEM = [['',u'分类'],['1001',u'娱乐'],['1002',u'体育'],['1003',u'新闻'],['1004',u'搞笑'],\
#                      ['1005',u'汽车'],['1006',u'母婴'],['1007',u'旅游'],['1008',u'时尚'],['1009',u'健康'],\
#                      ['1010',u'科技'],['1011',u'游戏'],['1012',u'游戏中心'],['1013',u'美女'],['1014',u'其他'],\
#                      ['1015',u'电影片花'],['1016',u'电视片花'],['1017',u'综艺片花'],['1018',u'动漫片花'],['1019',u'纪录片'],\
#                      ['1020',u'热点'],['1021',u'公开课'],['1022',u'财经'],['1023',u'音乐'],['1024',u'youtube精选'],\
#                      ['1025',u'国际'],['1026',u'军事'],['1027',u'广场舞'],['1028',u'广告'],['1029',u'生活'],\
#                      ['1030',u'梦之声'],['1031',u'ios淘宝'],['1032',u'android淘'],['1033',u'生活百科'],['5',u'微电影']]
step_id_rep = {'0':u'初始','10':u'下载','20':u'发送','30':u'提交','40':u'转码','50':u'审核','60':u'打包','70':u'分发'}
status_rep = {'0': u'中','1': u'成功', '2': u'失败', '3': u'敏感', '4': u'被拒绝', '6': u'被丢弃', '7': u'内部出错'}

def get_task_representation(step, status):
    step = str(step)
    status = str(status)

    part1 = step_id_rep[step] if step in step_id_rep else ''
    part2 = status_rep[status] if status in status_rep else ''
    return part1 + part2

@login_required
def nav_tree(request):
    username = request.user.username
    logger.info("%s login",username)
    return render_to_response("nav_tree.html", locals(), context_instance=RequestContext(request))

@login_required
def welcome(request):
    return render_to_response("welcome.html")

@csrf_exempt
@login_required
#@permission_required("subscribe.view_youtube",login_url="/forbidden/")
def youtube(request):
    username = request.user.username
    if 'show_id' in request.POST:
        show_id = request.POST['show_id'].encode('utf8')
        action = request.POST['action']
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        verify = Ordered.objects.filter(show__show_id = show_id)
        if action == "add": 
            if verify.count() == 0:
                owner = Owner.objects.get(show_id = show_id)
                user0 = request.POST['xuan']
                add = Ordered(show=owner, user=user0, ctime=now, site_id='2')
                add.save()
                logger.info(u"%s订阅YouTube中的show_id:%s,分类为:%s",username,show_id,user0)
        elif action == "cancel":
            if verify.count() > 0:
                verify.delete()
                logger.info(u"%s取消订阅YouTube中的show_id:%s",username,show_id)
        elif action == "manual":
            youtube_spider = ('youtube_hottest',)
            url = request.POST['url']
            user = request.POST['xuan']
            orders = '[{"url":"%s", "user":"%s"}]' % (url, user)
            orders = json.dumps(orders)
            for spider in youtube_spider:
                command = SCRAPYD_COMMAND + " -d orders=%s" 
                os.system(command % (spider, orders))
            logger.info(u"%s,手动启动频道订阅，URL:%s, 分类为:%s",username, url, user)

    order = request.GET.get('order', '').encode("utf8")
    status = request.GET.get('status', '').encode("utf8")
    classifi = request.GET.get('classifi', '').encode("utf8")
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    cond = request.GET.get('cond','').encode("utf8")
    content = request.GET.get('content','').encode("utf8")

    video_dao = UgcVideoDao.instance()
    video_list = video_dao.get_youtube(page, count, order, status, cond, content, classifi)
    video_total = int(video_dao.get_youtube_count(order, status, cond, content, classifi))
    
    sub_datas = video_dao.get_sub_showid_list()
    sub_dict = {}
    for sub_data in sub_datas:
        sub_dict[sub_data[0]] = sub_data[1]
    
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    order_item = order_ITEM
    status_item = status_ITEM
    classifi_item = classifi_ITEM
    search_item = [['', u'搜索类型'], ['user_name', u'源频道'], ['intro', u'简介']]
    
    return render_to_response('youtube_list.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
#@permission_required("subscribe.view_youku",login_url="/forbidden/")
def youku(request):
    username = request.user.username
    if 'show_id' in request.POST:
        show_id = request.POST['show_id'].encode('utf8')
        action = request.POST['action']
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        verify = Ordered.objects.filter(show__show_id = show_id)
        if action == "add": 
            if verify.count() == 0:
                owner = Owner.objects.get(show_id = show_id)
                add = Ordered(show=owner, user='youku', ctime=now, site_id='1')
                add.save()
                logger.info(u"%s订阅优酷中的show_id:%s",username,show_id)
        elif action == "cancel":
            if verify.count() > 0:
                verify.delete()
                logger.info(u"%s取消订阅优酷中的show_id:%s",username,show_id)             
        elif action == "manual":
            youku_spider = ('youku_order',)
            url = request.POST['url']
            orders = '[{"url":"%s", "user":"%s"}]' % (url, '')
            orders = json.dumps(orders)
            for spider in youku_spider:
                command = SCRAPYD_COMMAND + " -d orders=%s" 
                os.system(command % (spider, orders))
            logger.info(u"%s,手动启动频道订阅，URL:%s",username, url)
    
    order = request.GET.get('order', '').encode("utf8")
    status = request.GET.get('status', '').encode("utf8")
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    cond = request.GET.get('cond','').encode("utf8")
    content = request.GET.get('content','').encode("utf8")

    video_dao = UgcVideoDao.instance()
    video_list = video_dao.get_youku(page, count, order, status, cond, content)
    video_total = int(video_dao.get_youku_count(order, status, cond, content))
    
    sub_datas = video_dao.get_sub_showid_list()
    sub_dict = {}
    for sub_data in sub_datas:
        sub_dict[sub_data[0]] = sub_data[1]
    
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    order_item = order_ITEM
    status_item = status_ITEM
    search_item = [['', u'搜索类型'], ['user_name', u'源频道'], ['intro', u'简介']]
    
    return render_to_response('youku_list.html', locals(), context_instance=RequestContext(request))

@login_required
def keyword(request):
    return render_to_response('keyword.html')

@login_required
def keyword_show(request): 
    #k = Keyword.objects.all()
    video_dao = UgcVideoDao.instance()
    k = video_dao.get_keyword_list()
    return render(request, 'keyword_show.html', {'keyword': k})

@login_required
@permission_required("subscribe.add_keyword",login_url="/forbidden/")
def keyword_add(request):
    classifi_item = classifi_ITEM
    video_dao = UgcVideoDao.instance()
    youku_item = video_dao.get_category_item('1')
    youtube_item = video_dao.get_category_item('2')
    ku6_item = video_dao.get_category_item('6')
    return render_to_response('keyword_add.html', locals(), context_instance=RequestContext(request))

@login_required
#@permission_required("subscribe.add_ordered",login_url="/forbidden/")
def add_order(request):
    username = request.user.username
    tip = ""
    if request.method == "POST":
        site = request.POST['site'].encode('utf8')
        channel = request.POST['channel']
        url = request.POST['url'].encode('utf8')

        if site != '0':
            url_match = re.findall(r"^http[s]?://(?:i.youku.com/u|www.youtube.com/(?:channel|user)?)?/.*", url)
            if url_match :
                #parse channel
                rel_url = '/api/parse?url=%s&type=channel' % urllib2.quote(url)
                req = request.build_absolute_uri(rel_url)
                ret = urllib2.urlopen(req).read()

                if ret:
                    ret_json = json.loads(ret)
                    if ret_json and ret_json['ret'] == '0':
                        show_id = ret_json['show_id']
                        user_name = ret_json['user_name']
                        intro = ret_json['intro']
                        now = time.strftime('%Y-%m-%d %H:%M:%S')

                        check_owner = Owner.objects.filter(show_id = show_id)
                        if check_owner.count() == 0:
                            #add a channel record
                            record = Owner(show_id=show_id, site_id=site, create_time=now, url=url, user_name=user_name, intro=intro)
                            record.save()

                        owner = Owner.objects.get(show_id = show_id)
                        record = Ordered(show=owner, user=channel, ctime=now, site_id=site)
                        record.save()
                        logger.info(u"%s添加了频道订阅，源频道:%s",username,user_name)

                        tip = "订阅成功！"
                    else:
                        tip = "无法解析频道！"
            else:
                tip = "无法匹配输入的URL，请重新输入！"
        else:
            tip = "请选择网站！"

    return render_to_response('add.html', locals(), context_instance=RequestContext(request))

@login_required
def page(request):
    return render_to_response('page.html')

@login_required
def page_show(request): 
    p = Page.objects.all()
    return render(request, 'page_show.html', {'page_info': p})

@login_required
@permission_required("subscribe.add_page",login_url="/forbidden/")
def page_add(request):
    classifi_item = classifi_ITEM
    return render_to_response('page_add.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def video(request): 
    origin = request.GET.get('origin', '').encode("utf8")
    classifi = request.GET.get('classifi', '').encode("utf8")
    order = request.GET.get('order','').encode("utf8")
    status = request.GET.get('status', '').encode("utf8")
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    cond = request.GET.get('cond','').encode("utf8")
    content = request.GET.get('content','').encode("utf8")

    video_dao = UgcVideoDao.instance()
    video_list = video_dao.get_episode_video(page, count, origin, classifi, status, order, cond, content)
    video_total = int(video_dao.get_episode_video_count(origin, classifi, status, cond, content))
    
    for v in video_list:
        v['result'] = get_task_representation(v['step_id'], v['status'])
        if not v['result']:
            v['result']=u'未处理'
    #print video_total
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items() 
    
    origin_item = [['',u'所有来源'],['1',u'优酷'],['2',u'YouTube'],['3',u'搜狐'],['4',u'凤凰'],['5',u'爱奇艺'],['6',u'酷6'],['100',u'风行']]
    classifi_item = classifi_ITEM
    status_item = [['',u'所有状态'],['0',u'进行中'],['1',u'成功'],['2',u'失败'],['3',u'被过滤'],['4',u'被拒绝'],['6',u'被丢弃'],['7',u'内部出错'],['8',u'未处理']]
    order_item = [['',u'排序方式'],['played',u'播放数'],['upload_time',u'上传时间'],['create_time',u'爬取时间']]
    search_item = [['',u'搜索类型'],['title',u'标题'],['user_name',u'源频道']]
    
    #send_dict = video_dao.get_send_showid_list(showids=[item['show_id'] for item in video_list])
    
    return render(request, 'video.html', locals(), context_instance=RequestContext(request))

@login_required
def copyright_channel(request):
    return render_to_response('copyright_channel.html')

@login_required
def copyright_channel_show(request): 
    cc = ChannelExclude.objects.all()
    return render(request, 'copyright_channel_show.html', {'copyright_channel': cc})

@login_required
@permission_required("subscribe.add_copyright_channel",login_url="/forbidden/")
def copyright_channel_add(request):
    #classifi_item = classifi_ITEM
    return render_to_response('copyright_channel_add.html', locals(), context_instance=RequestContext(request))

@login_required
def cat(request):
    return render_to_response('cat.html')

@login_required
def cat_show(request): 
    cat_info = CatList.objects.all()
    return render_to_response('cat_show.html', locals(), context_instance=RequestContext(request))

@login_required
@permission_required("subscribe.add_cat",login_url="/forbidden/")
def cat_add(request):
    return render_to_response('cat_add.html', locals(), context_instance=RequestContext(request))

@login_required
def subject(request):
    return render_to_response('subject.html')

@login_required
def subject_show(request): 
    subject_info = Subject.objects.all()
    return render_to_response('subject_show.html', locals(), context_instance=RequestContext(request))

@login_required
@permission_required("subscribe.add_subject",login_url="/forbidden/")
def subject_add(request):
    return render_to_response('subject_add.html', locals(), context_instance=RequestContext(request))

