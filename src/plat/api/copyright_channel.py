#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import StreamingHttpResponse
from subscribe.models import ChannelExclude
import json
import time
import re
import urllib2
import logging
logger = logging.getLogger('my')

def cc(request, op):
    username = request.user.username
    try:
        ret = ""
        if op == "cancel":
            user = request.GET.get('user_name')
            if user:
                rec = ChannelExclude.objects.filter(user_name=user)
                if not rec:
                    ret = u"频道  %s not exist" % user
                else:
                    rec.delete()
                    ret = "ok"
                    logger.info(u"%s取消了版权频道限制，频道名称：%s",username,user)
            else:
                ret = u"missing 频道名称"
            
        elif op == "add":
            user = request.GET.get('user')
            url = request.GET.get('url')
            
            if user:
                rec = ChannelExclude.objects.filter(user_name=user)
                if rec:
                    ret = u"频道   %s exist" % user
                else:
                    
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

                                channel_add = ChannelExclude(show_id=show_id,user_name=user, url=url)
                                channel_add.save()
                                ret = "ok"
                                logger.info(u"%s添加了版权频道限制，频道名称：%s",username,user)
        
                                ret = u"成功！"
                            else:
                                ret = u"无法解析频道！"
                    else:
                        ret = u"无法匹配输入的URL，请重新输入！"
            else:
                ret = u"missing 频道"
        else:
            ret = "not supported operation %s" % op.split('/')[0]

        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))

    