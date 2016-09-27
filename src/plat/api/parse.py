#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import re
import json
import urllib2
import urllib
from django.http import HttpResponse
from plat.settings import PROXY_SERVER

def do_parse(url, tp='video'):
    #check scheme
    if not check_scheme(url):
        return {"ret": "1", "msg": u"None http/https schema"}

    #parse
    site = get_site(url)
    try:
        parser = getattr(sys.modules[__name__], "parse_url_%s_%s" % (site, tp))
    except Exception, e:
        return {"ret": "1", "msg": u"Not support: %s, %s" % (site, tp)}

    try:
        ret = parser(url, site)
        return ret
    except Exception, e:
        return {"ret": "1", "msg": u"Cannot parse url: %s" % (url,)}

def parse_url(request):
    url = request.GET.get("url", "").strip()
    tp = request.GET.get("type", "video")

    ret = do_parse(url, tp)

    return HttpResponse(json.dumps(ret))

def check_scheme(url):
    return url[:4] == "http"

def get_site(url):
    r = re.compile('^.*://\w+\.(\w+).\w+/.*$')
    m = r.match(url)
    if m:
        return m.group(1)
    return ""

def parse_url_base(url, pattern, site):
    res = {"msg":u" ", "ret": "0", "site": site}
    try:
        if site == 'youtube':
            proxy = urllib2.ProxyHandler({'https': PROXY_SERVER, 'http': PROXY_SERVER})
            _opener = urllib2.build_opener(proxy)
        else:
            _opener = urllib2.build_opener()
        response = _opener.open(url, timeout = 30)
        if response.getcode() == 200:
            content = response.read()
            response.close()

            for (k, v) in pattern.items():
                for r in v:
                    m = r.findall(content)
                    if m:
                        res[k] = m[0]
                        if not res[k]:
                            res[k] = u""
                        break
                    res[k] = u""
    except Exception, e:
        res = {"ret": "1", "msg": "parse get exception"}
        print e
    return res

def parse_url_youku_video(url, site):
    pattern = {'show_id':[re.compile(r'videoId2 ?= \'(.+?)\';', re.S)], 'title': [re.compile(r'<span id="subtitle">(.*?)</span>', re.S), re.compile(r'<h1 class="title".*?>(.*?)</h1>', re.S)], 'tag': [re.compile(r'var tags="(.*?)";', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<div class="crumbs">.*?<a.*?>(.*?)</a>.*?</div>', re.S)]}
    ret = parse_url_base(url, pattern, site)

    if ret and ret['tag']:
        ret['tag'] = urllib.unquote(ret['tag'].encode('utf8')).decode('utf8').rstrip('|')
    return ret

def parse_url_tudou_video(url, site):
    pattern = {'show_id':[re.compile(r'icode: \'(.+?)\'', re.S)], 'title': [re.compile(r'<h1 class="kw".*>(.*?)</h1>', re.S)], 'tag': [re.compile(r"tag: '(.*?)'", re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="v_channel">.*?<a.*?>(.*?)</a>.*?</span>', re.S)]}
    ret = parse_url_base(url, pattern, site)

    for k, v in ret.items():
        ret[k] = v.decode('utf8')

    if ret and ret['tag']:
        ret['tag'] = ret['tag'].replace(',', '|')

    return ret

def parse_url_56_video(url, site):
    pattern = {'show_id':[re.compile(r'"EnId":"(.+?)"', re.S)], 'title': [re.compile(r'<span id="vh_title_text".*?>(.*?)</span>', re.S), re.compile(r'<h1 id="video_title_text".*>(.*?)</h1>', re.S)], 'tag': [re.compile(r'"tags":"(.*?)"', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="crumbs">.*?<a .*?>.*?</a>.*?<a .*?>(.*?)</a>.*?</span>', re.S), re.compile(r'<span class="crumb">.*?<a .*?>.*?</a>.*?<a .*?>(.*?)</a>.*?</span>', re.S)]}
    ret = parse_url_base(url, pattern, site)

    #decode
    if ret and ret['tag']:
        ret['tag'] = ret['tag'].decode('unicode-escape').replace(',', '|')

    return ret

def parse_url_ku6_video(url, site):
    pattern = {'show_id':[re.compile(r', id: "(.+?)",', re.S)], 'title': [re.compile(r'title: "(.*?)"', re.S)], 'tag': [re.compile(r'tag: "(.*?)"', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="ckl_chane">.*?<a .*?>(.*?)</a>.*?</span>', re.S)]}
    ret = parse_url_base(url, pattern, site)

    #decode
    if ret and ret['title']:
        ret['title'] = ret['title'].decode('unicode-escape')
    if ret and ret['tag']:
        ret['tag'] = ret['tag'].decode('unicode-escape').replace(' ', '|').replace(',', '|').rstrip('|')
    if ret and ret['description']:
        ret['description'] = ret['description'].decode('gbk')
    if ret and ret['channel']:
        ret['channel'] = ret['channel'].decode('gbk')

    return ret

def parse_url_youtube_video(url, site):
    pattern = {'show_id':[re.compile(r'"vid": "(.+?)"', re.S)], 'title': [re.compile(r'<meta property="og:title" content="(.*?)"', re.S), ], 'tag': [re.compile(r'<meta name="keywords" content="(.*?)"', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)],}
    ret = parse_url_base(url, pattern, site)

    if 'show_id' not in ret or not ret['show_id']:
        r = re.compile(r'https?://www.youtube.com/watch\?v=([^&]+)')
        m = r.match(url)
        if m:
            ret['show_id'] = m.group(1)

    if ret and ret['tag']:
        ret['tag'] = ret['tag'].replace(',', '|')
    return ret

def parse_url_iqiyi_video(url, site):
    pattern = {'title': [re.compile(r'<meta name="title" content="(.*?)"', re.S), ], 'tag': [re.compile(r'<meta name="keywords" content="(.*?)"', re.S)], 'description': [re.compile(r'<meta  name="description" content="(.*?)"', re.S)],}
    ret = parse_url_base(url, pattern, site)

    #get show id
    r = re.compile('http://www.iqiyi.com/(.*?).html')
    m = r.match(url)
    if m:
        ret['show_id'] = m.group(1)

    if ret and ret['tag']:
        ret['tag'] = ret['tag'].replace(',', '|').replace('，', '|')
    return ret

def parse_url_youku_channel(url, site):
    pattern = {'show_id': [re.compile(r'ownerEncodeid = \'(.*?)\';', re.S)], 'user_name': [re.compile(r'<div class="username">.*?<a .*?>(.*?)</a>.*?</div>', re.S)], 'intro': [re.compile(r'<div class="desc">.*?<p>.*?</p>.*?<p>(.*?)</p>.*?</div>', re.S)]}
    ret = parse_url_base(url, pattern, site)

    return ret

def parse_url_youtube_channel(url, site):
    pattern = {'show_id': [re.compile(r'\(\'CHANNEL_ID\', "(.*?)"\)', re.S)], 'user_name': [re.compile(r'<meta property="og:title" content="(.*?)">', re.S)], 'intro': [re.compile(r'<meta name="twitter:description" content="(.*?)">', re.S)]}
    ret = parse_url_base(url, pattern, site)

    return ret

if __name__ == "__main__":
    url1 = ["http://v.youku.com/v_show/id_XNzIzNzYwMjY4.html", 
            "http://www.tudou.com/programs/view/g3SZOD8p-ss/?FR=LIAN", 
            "http://www.56.com/u96/v_MTE4MTgxMjY5.html", 
            "http://www.56.com/u63/v_MTIwMzg3OTI0.html", 
            "http://v.ku6.com/show/Ujby2SQ8pl9_FqgR1TB0Sg...html?hpsrc=1_24_1_1_0",
            "https://www.youtube.com/watch?v=Qam4iiya1q0",
            "https://www.youtube.com/watch?v=Gu6aqm8z-GE",
            ]

    url2 = ["http://i.youku.com/u/UNTY0ODU3NTI4",
            "https://www.youtube.com/channel/UCPDXXXJj9nax0fr0Wfc048g",
            "https://www.youtube.com/user/collegehumor",
            "http://www.youtube.com/channel/UCPDXXXJj9nax0fr0Wfc048g",
            "http://www.youtube.com/user/collegehumor",
            ]
    
    for u in url1:
        site = get_site(u)
        try:
            parser = getattr(sys.modules[__name__], "parse_url_%s_%s" % (site, "video"))
            print json.dumps(parser(u, site))
        except Exception, e:
            print "exception: %s" % e

    for u in url2:
        site = get_site(u)
        try:
            parser = getattr(sys.modules[__name__], "parse_url_%s_%s" % (site, "channel"))
            print json.dumps(parser(u, site))
        except Exception, e:
            print "exception: %s" % e
