#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import StreamingHttpResponse
from subscribe.models import Keyword
from subscribe.models import Page
from subscribe.models import CatList
from subscribe.models import Subject
from subscribe.models import Site
from plat.settings import DATA_SERVER_IP, DATA_SERVER_PORT, SCRAPYD_COMMAND
from db.db_datas import DBDatas
from plat.common import cal_fit
import urllib2
import httplib
import json
import time
import os
import logging
logger = logging.getLogger('my')

# Create your views here.
def subscribe_keyword(request, op):
    username = request.user.username
    try:
        ret = ""
        if op == "cancel":
            #get query parameter
            id = request.GET.get('keyword').split('|')[0]
            key = request.GET.get('keyword').split('|')[1]
            #print id,key

            if key:
                rec = Keyword.objects.filter(id=id)
                if not rec:
                    ret = "keyword %s not exist" % key
                else:
                    rec.delete()
                    ret = "ok"
                    logger.info(u"用户:%s 取消了关键词订阅，关键词：%s",username,key)
            else:
                ret = "missing keyword"

        elif op == "add":
            #get query parameter
            key = request.GET.get('keyword')
            user = request.GET.get('user')
            tp = request.GET.get('type', 'video')
            site = request.GET.get('site')
            cat_id = request.GET.get('cat_id','')
            #print 'cat_id:',cat_id

            if key:
                rec = Keyword.objects.filter(keyword=key,site_id=site)
                if rec:
                    ret = "keyword %s already exists in this site" % key
                else:
                    key_add = Keyword(keyword=key, user=user, type=tp, site_id=site, ext_cat_id=cat_id)
                    key_add.save()
                    ret = "ok"
                    logger.info(u"用户:%s 添加了关键词订阅，关键词：%s",username,key)
            else:
                ret = "missing keyword"

        elif op == "manual":
            keyword_spider={'youku':('youku_search_video',), 'youtube':('youtube_search_video',), 'iqiyi':('iqiyi_search_video',), 'ku6':('ku6_search_video',)}
            site = request.GET.get('site')
            user = request.GET.get('user')
            kw_id = request.GET.get('keyword').split('|')[0]
            keyword = request.GET.get('keyword').split('|')[1]
            cat_id = request.GET.get('cat_id')
            site = Site.objects.get(site_id=site)
            if site:
                if site.site_name in keyword_spider.keys():
                    keywords = '[{"id":"%s", "keyword":"%s", "user":"%s", "ext_cat_id":"%s"}]' % (kw_id, keyword, user, cat_id)
                    keywords = json.dumps(keywords)
                    spiders = keyword_spider[site.site_name]
                    for spider in spiders:
                        command = SCRAPYD_COMMAND + " -d cat_ids=%s -d keywords=%s"
                        os.system(command % (spider, None, keywords))
                    ret = "ok"
                    logger.info(u"用户:%s 手动启动关键词订阅，关键词：%s",username,keyword)
                else:
                    ret = "not support for %s(%s)" % (site.site_name, site.site_id)
            else:
                ret = "missing site_id"

        else:
            ret = "not supported operation %s" % op.split('/')[0]

        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))

def subscribe_page(request, op):
    username = request.user.username
    try:
        ret = ""
        if op == "cancel":
            #get query parameter
            id = request.GET.get('page_url').split('|')[0]
            key = request.GET.get('page_url').split('|')[1]

            if key:
                rec = Page.objects.filter(id=id)
                if not rec:
                    ret = "page_url %s not exist" % key
                else:
                    rec.delete()
                    ret = "ok"
                    logger.info(u"用户:%s 取消了页面订阅，URL：%s",username,key)
            else:
                ret = "missing page_url"

        elif op == "add":
            #get query parameter
            url = request.GET.get('url')
            user = request.GET.get('user')
            #ctime = request.GET.get('ctime')
            ctime = time.strftime('%Y-%m-%d %H:%M:%S')
            site = request.GET.get('site')

            if url:
                rec = Page.objects.filter(url=url)
                if rec:
                    ret = "URL %s EXIST" % url
                else:
                    page_add = Page(url=url, user=user, ctime=ctime)
                    page_add.site_id = site
                    page_add.save()
                    ret = "OK"
                    logger.info(u"用户:%s 添加了页面订阅，URL：%s",username,url)
            else:
                ret = "missing page_url"

        elif op == "manual":
            page_spider={'youku':('page_order',), 'iqiyi':('page_order',)}
            site = request.GET.get('site')
            page_id = request.GET.get('page_id', '')
            user = request.GET.get('user')
            url = request.GET.get('url').split('|')[1]
            site = Site.objects.get(site_id=site)
            if site:
                if site.site_name in page_spider.keys():
                    orders = '[{"id":"%s", "url":"%s", "user":"%s", "site_id":"%s"}]' % (page_id, urllib2.quote(url), user, site.site_id)
                    orders = json.dumps(orders)
                    spiders = page_spider[site.site_name]
                    for spider in spiders:
                        command = SCRAPYD_COMMAND + " -d orders=%s"
                        os.system(command % (spider, orders))
                    ret = "ok"
                    logger.info(u"用户:%s 手动启动页面订阅，URL：%s",username, url)
                else:
                    ret = "not support for %s(%s)" % (site.site_name, site.site_id)
            else:
                ret = "missing site_id"
        
        else:
            ret = "not supported operation %s" % op.split('/')[0]

        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))
    
def subscribe_cat(request, op):
    username = request.user.username
    try:
        ret = ""
        if op == "cancel":
            #get query parameter
            key = request.GET.get('cat_url')

            if key:
                rec = CatList.objects.filter(url=key)
                if not rec:
                    ret = "cat_url %s not exist" % key
                else:
                    rec.delete()
                    ret = "ok"
                    logger.info(u"用户:%s 取消了分类页订阅，URL：%s",username,key)
            else:
                ret = "missing cat_url"

        elif op == "add":
            #get query parameter
            url = request.GET.get('url')
            user = request.GET.get('user')
            site = request.GET.get('site')
            if url:
                rec = CatList.objects.filter(url=url)
                if rec:
                    ret = "URL %s EXIST" % url
                else:
                    cat_add = CatList(url=url, cat_name=user, site_id=site)
                    cat_add.save()
                    ret = "OK"
                    logger.info(u"用户:%s 添加了分类页订阅，URL：%s",username,url)
            else:
                ret = "missing cat_url"

        elif op == "manual":
            cat_spider={'youku':('youku_cat_hottest', 'youku_cat_newest'), 'iqiyi':('iqiyi_military_hottest',)}
            site = request.GET.get('site')
            url = request.GET.get('url')
            cat_id = request.GET.get('cat_id', '')
            site = Site.objects.get(site_id=site)
            if site:
                if site.site_name in cat_spider.keys():
                    cat_urls = '[{"id":"%s", "url":"%s"}]' % (cat_id, url)
                    cat_urls = json.dumps(cat_urls)
                    spiders = cat_spider[site.site_name]
                    for spider in spiders:
                        command = SCRAPYD_COMMAND + " -d cat_urls=%s"
                        os.system(command % (spider, cat_urls))
                    ret = "ok"
                    logger.info(u"用户:%s 手动启动分类订阅，URL：%s",username, url)
                else:
                    ret = "not support for %s(%s)" % (site.site_name, site.site_id)
            else:
                ret = "missing site_id"
        
        else:
            ret = "not supported operation %s" % op.split('/')[0]

        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))
    
def subscribe_subject(request, op):
    username = request.user.username
    try:
        ret = ""
        if op == "cancel":
            #get query parameter
            key = request.GET.get('subject_url')
            print key
            if key:
                rec = Subject.objects.filter(url=key)
                if not rec:
                    ret = "subject_url %s not exist" % key
                else:
                    rec.delete()
                    ret = "ok"
                    logger.info(u"用户:%s 取消了专题订阅，URL：%s",username,key)
            else:
                ret = "missing subject_url"

        elif op == "add":
            #get query parameter
            url = request.GET.get('url')
            sub = request.GET.get('subject')
            user = request.GET.get('user')
            site = request.GET.get('site')

            if url:
                rec = Subject.objects.filter(url=url)
                if rec:
                    ret = "URL %s EXIST" % url
                else:
                    subject_add = Subject(url=url, subject_name=sub,cat_name=user, site_id=site)
                    subject_add.save()
                    ret = "OK"
                    logger.info(u"用户:%s 添加了专题订阅，URL：%s",username,url)
            else:
                ret = "missing subject_url"

        elif op == "manual":
            subject_spider={'iqiyi':('iqiyi_subject_history',)}
            site = request.GET.get('site')
            url = request.GET.get('url')
            subject = request.GET.get('subject')
            subject_id = request.GET.get('subject_id', '')
            site = Site.objects.get(site_id=site)
            if site:
                if site.site_name in subject_spider.keys():
                    cat_urls = '[{"id":"%s", "subject_name":"%s", "url":"%s"}]' % (subject_id, subject, url)
                    cat_urls = json.dumps(cat_urls)
                    spiders = subject_spider[site.site_name]
                    for spider in spiders:
                        command = SCRAPYD_COMMAND + " -d cat_urls=%s"
                        os.system(command % (spider, cat_urls))
                    ret = "ok"
                    logger.info(u"用户:%s 手动启动专题订阅，专题名词：%s，URL: %s",username, subject, url)
                else:
                    ret = "not support for %s(%s)" % (site.site_name, site.site_id)
            else:
                ret = "missing site_id"
        
        else:
            ret = "not supported operation %s" % op.split('/')[0]

        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))

def send_episode(request): 
    ret = ""

    try:
        if 'show_id' in request.GET:
            show_id = request.GET.get('show_id', '').encode("utf8")
            force = request.GET.get('force', '0')
            user = request.GET.get('user', 'unknown')
            url = "/op/sendepisode?sid=%s&audit=1&priority=6&force=%s" % (show_id, force)
            try:
                conn = httplib.HTTPConnection(DATA_SERVER_IP, DATA_SERVER_PORT)
                conn.request('GET',url)
                ret = "ok"
                logger.info(u"用户:%s 向data_server提交,show_id:%s", user, show_id)
            except Exception, e:
                ret = str(e)
    except Exception, e:
        logger.error(e)
        ret = str(e)
           
    return StreamingHttpResponse(json.dumps({'ret': ret}))

def fix_funshion(request):
    username = request.user.username
    ret = ""
    try:
        fun_id = request.GET.get('media_id', '')
        dou_id = request.GET.get('show_id','')

        if fun_id and dou_id:
            xv_dao = DBDatas.instance()
            douban_detail = xv_dao.get_douban_detail(dou_id)

            xv_dao.update_funshion_detail(fun_id, title=douban_detail['title'], director=douban_detail['director'], actor=douban_detail['actor'], category=douban_detail['type'])
            
            fun_detail = xv_dao.get_funshion_detail(fun_id)
            fit = cal_fit(fun_detail, douban_detail)

            xv_dao.update_fun_dou_fit(fun_id, dou_id, fit)
            
            logger.info(u"用户:%s 执行了一键修复操作，风行ID:%s, 豆瓣ID:%s ",username,fun_id,dou_id)

            ret = "ok"

    except Exception, e:
        logger.error(e)
        ret = str(e)

    return StreamingHttpResponse(json.dumps({'ret': douban_detail}))
