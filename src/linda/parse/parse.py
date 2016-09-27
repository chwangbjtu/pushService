#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import re
import json
import urllib2
import urllib
from cStringIO import StringIO
import gzip
reload(sys) 

sys.setdefaultencoding('utf-8')
#from django.http import HttpResponse
def gunzip(data):
    inbuffer = StringIO(data)
    f = gzip.GzipFile(mode="rb", fileobj=inbuffer)
    rdata = f.read()
    return rdata

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

    #return HttpResponse(json.dumps(ret))
    return json.dumps(ret)

def check_scheme(url):
    return url[:4] == "http"

def get_site(url):
    try:
        special_site = ['61', 'kumi']
        for s in special_site:
            if url.startswith('http://%s.' % s):
                return s

        r = re.compile('http[s]{0,1}://.+\.(.*?)\.(com.cn)')
        m = r.match(url.split('?')[0])
        if m:
            return m.group(1)

        r = re.compile('http[s]{0,1}://.+\.(.*?)\.[com|cn|tv]')
        m = r.match(url.split('?')[0])
        if m:
            return m.group(1)
        return ""
    except Exception as e:
        print traceback.format_exc()

def parse_url_base(url, pattern, site):
    res = {"retmsg":u"ok", "retcode": "200"}
    try:
        if site == 'youtube':
            proxy = urllib2.ProxyHandler({'https': '125.88.157.17:37349', 'http': '125.88.157.17:37349'})
            _opener = urllib2.build_opener(proxy)
        else:
            _opener = urllib2.build_opener()
        response = _opener.open(url, timeout = 30)
        if response.getcode() == 200:
            content = response.read()
            response.close()
            if site == 'bilibili':
                content = gunzip(content)
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
        res = {"retcode": "404", "retmsg": "parse get exception"}
        print e
    return res

def parse_url_youku_video(url, site):
    pattern = {'show_id':[re.compile(r'videoId2 ?= \'(.+?)\';', re.S)], 'title': [re.compile(r'<span id="subtitle">(.*?)</span>', re.S), re.compile(r'<h1 class="title".*?>(.*?)</h1>', re.S)], 'tag': [re.compile(r'var tags="(.*?)";', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<div class="crumbs">.*?<a.*?>(.*?)</a>.*?</div>', re.S)]}
    ret = parse_url_base(url, pattern, site)

    if ret and ret['tag']:
        ret['tag'] = urllib.unquote(ret['tag'].encode('utf8')).decode('utf8').rstrip('|')
    return ret

def parse_url_tudou_video(url, site):
    #pattern = {'show_id':[re.compile(r'icode: \'(.+?)\'', re.S)], 'title': [re.compile(r'<h1 class="kw".*>(.*?)</h1>', re.S)], 'tag': [re.compile(r"tag: '(.*?)'", re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="v_channel">.*?<a.*?>(.*?)</a>.*?</span>', re.S)]}
    pattern = {'show_id':[re.compile(r'icode:\s+\'(.+?)\'', re.S)], 'title': [re.compile(r'<h1 class="kw"\s+id="\w+" title="(.*?)">', re.S)], 'tag': [re.compile(r'(?i)<meta name="keywords" content="(.*?)"', re.S)], 'description': [re.compile(r'(?i)<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<meta name="irCategory" content="(.*?)"', re.S)]}
    ret = parse_url_base(url, pattern, site)

    for k, v in ret.items():
        ret[k] = v.decode('utf8')
    if ret and ret['tag']:
        ret['tag'] = ret['tag'].replace(',', '|').strip('|')

    return ret

def parse_url_56_video(url, site):
    try:
        pattern = {'show_id':[re.compile(r'"EnId":"(.+?)"', re.S)], 'title': [re.compile(r'<span id="vh_title_text".*?>(.*?)</span>', re.S), re.compile(r'<h1 id="video_title_text".*>(.*?)</h1>', re.S)], 'tag': [re.compile(r'"tags":"(.*?)"', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="crumbs">.*?<a .*?>.*?</a>.*?<a .*?>(.*?)</a>.*?</span>', re.S), re.compile(r'<span class="crumb">.*?<a .*?>.*?</a>.*?<a .*?>(.*?)</a>.*?</span>', re.S)]}
        ret = parse_url_base(url, pattern, site)
        #decode
        if ret and ret['tag']:
            ret['tag'] = ret['tag'].decode('unicode-escape').replace(' ', '|').replace(',', '|').rstrip('|')

        return ret
    except Exception, e:
        log.app_log.info(traceback.format_exc())

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
    #pattern = {'title': [re.compile(r'<meta name="title" content="(.*?)"', re.S), ], 'tag': [re.compile(r'(?i)<meta name="keywords" content="(.*?)"', re.S)], 'description': [re.compile(r'<meta\s+name="description" content="(.*?)"', re.S)],'channel': [re.compile(r'<meta  name="irCategory" content="(.*?)"', re.S)]}
    pattern = {'title': [re.compile(r'<meta name="title" content="(.*?)"', re.S), ], 'tag': [re.compile(r'(?i)<meta name="keywords" content="(.*?)"', re.S)], 'description': [re.compile(r'<meta\s+name="description" content="(.*?)"', re.S)],'channel': [re.compile(r'<meta  name="irCategory" content="(.*?)"', re.S)]}
    ret = parse_url_base(url, pattern, site)

    #get show id
    r = re.compile('http://www.iqiyi.com/(.*?).html')
    m = r.match(url)
    if m:
        ret['show_id'] = m.group(1)

    if ret and ret['tag']:
        ret['tag'] = ret['tag'].replace(',', '|').replace('，', '|')
    return ret


def parse_url_v1_video(url, site):
    #pattern = {'title': [re.compile(r'<h1 class="topTitle">(.*?)</h1>', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'<dd><a href="http://www.v1.cn/" target="_blank">(.*?)</a></dd>', re.S),re.compile(r'index.shtml" target="_blank" title="(.*?)"', re.S)]}
    pattern = {'title': [re.compile(r'<h1 class="topTitle">(.*?)</h1>', re.S)],'tag':[re.compile(r' <a class="videoTag" target="_blank" href=".*?" tags="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'<dd><a href=".*?" target="_blank">(.*?)</a></dd>', re.S),re.compile(r'index.shtml" target="_blank" title="(.*?)"', re.S)]}
    ret = parse_url_base(url, pattern, site)
    r = re.compile(r'http://.+/(\d+).shtml')
    m = r.match(url)
    if m:
        ret['show_id'] = m.group(1)
    return ret
def parse_url_ifeng_video(url, site):
    #pattern = {'title': [re.compile(r'<meta property="og:title" content="(.*?)"', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta property="og:description" content="(.*?)"', re.S)],'channel':[re.compile(r'<meta name="irCategory" content="(.*?)"', re.S)]}
    pattern = {'title': [re.compile(r'<meta property="og:title" content="(.*?)"', re.S)],'tag':[re.compile(r'标签：(.*</a>)\s+\n', re.S)],'description':[re.compile(r'<meta property="og:description" content="(.*?)"', re.S)],'channel':[re.compile(r'<meta name="irCategory" content="(.*?)"', re.S)]}
    ret = parse_url_base(url, pattern, site)
    if 'tag' in ret :
        temp_tag = ret['tag']
        temp_tag_list = temp_tag.split('</a>')
        tags = []
        for tag_str in temp_tag_list:
            sub_list = tag_str.split('>') if tag_str else None
            tag = sub_list[1] if sub_list and len(sub_list) == 2 else None
            if tag:
                tags.append(tag)
                
        ret['tag'] = '|'.join(tags)
    
    tmp = url.split("/")[-1]
    tmp = tmp.split('.')[0]
    ret['show_id'] = tmp.replace("-", "")
    return ret
def parse_url_acfun_video(url, site):
    #pattern = {'title': [re.compile(r'<h1 id="txt-title-view">(.*?)</h1>', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'<a href="/">主页</a> > <a href="/v/list\d+/index.htm">(.*?)</a>', re.S)]}
    pattern = {'title': [re.compile(r'<h1 id="txt-title-view">(.*?)</h1>', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'<a href="/">主页</a>.*?<a href="/v/list.*?/index.htm">(.*?)<', re.S)]}
    ret = parse_url_base(url, pattern, site)
    if 'description' in ret :
        i = ret['description'].find('<')
        ret['description'] = ret['description'][:i]
    for v in ret:
        if v in ('title','tag','channel','channel','description'):
            ret[v]=unicode(ret[v], errors='ignore')
    r = re.compile(r'http://.+/ac(\d+)')
    m = r.match(url)
    if m:
        ret['show_id'] = m.group(1)
    return ret
def parse_url_bilibili_video(url, site):
    #pattern = {'title': [re.compile(r'<title>(.*?)</title>', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'class="on" rel="v:url" property="v:title">(.*?)</a>', re.S)]}
    pattern = {'title': [re.compile(r'<h1 title="(.*?)"', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'html\'  rel="v:url" property="v:title">(.*?)</a>', re.S)]}
    ret = parse_url_base(url, pattern, site)
    
    r = re.compile(r'http://.+/av(\d+)/')
    m = r.match(url)
    if m:
        ret['show_id'] = m.group(1)
    return ret
def parse_url_tucao_video(url, site):
    pattern = {'title': [re.compile(r'<h1 class="show_title">(.*?)<b id="title_part">', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'class="sub_on" >(.*?)</a>', re.S)]}
    ret = parse_url_base(url, pattern, site)
    r = re.compile(r'http://.+/h(\d+)/')
    m = r.match(url)
    ret['title'] =ret['title'].split('<')[0] 
    if m:
        ret['show_id'] = m.group(1)
    return ret
def parse_url_letv_video(url, site):
    pattern = {'title': [re.compile(r'<meta name="irTitle" content="(.*?)"', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'<meta name="irCategory" content="(.*?)"', re.S)]}
    ret = parse_url_base(url, pattern, site)
    r = re.compile(r'http://.+/(\d+).html')
    m = r.match(url)
    if m:
        ret['show_id'] = m.group(1)
    return ret
def parse_url_sohu_video(url, site):
    pattern = {'title': [re.compile(r'<meta property="og:title" content="(.*?)"', re.S)],'tag':[re.compile('<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'<meta name="category" content="(.*?)"', re.S)]}
    ret = parse_url_base(url, pattern, site)
    r = re.compile(r'http://.+/n(\d+).shtml')
    m = r.match(url)
    if m:
        ret['show_id'] = m.group(1)
    ret['title']=ret['title'].split('-')[0]
    #ret = json.dumps(ret)
    for v in ret:
        ret[v]=ret[v].decode('gb2312').encode('utf-8')
    return ret
def parse_url_hunantv_video(url, site):
    pattern = {'title': [re.compile(r'<title>(.*?)</title>', re.S)],'tag':[re.compile(r'<meta name="keywords" content="(.*?)"', re.S)],'description':[re.compile(r'<meta name="description" content="(.*?)"', re.S)],'channel':[re.compile(r'<a href="http://list.mgtv.com/.*?">(.*?)</a>\r\n<i>', re.S)]}
    ret = parse_url_base(url, pattern, site)
    r = re.compile(r'http://.+/(\d+).html')
    m = r.match(url)
    ret['channel']=ret['channel'].replace('\r\n','')
    if m:
        ret['show_id'] = m.group(1)
    return ret
class parse(object):
    def __init__(self):
        pass
    def handle(self, url):
        url = urllib.unquote(url)
        site = get_site(url)
        if site=='le':
            site='letv'
        if site=='mgtv':
            site='hunantv'
        try:
            parser = getattr(sys.modules[__name__], "parse_url_%s_%s" % (site, "video"))
            res = parser(url, site)
            return json.dumps(res)
        except Exception, e:
            return {"retcode":"404","retmsg":"not found "}
        
if __name__ == "__main__":
    url = [
            "http://v.ifeng.com/news/taiwan/201604/01e4861b-5983-474a-9e60-f4b6e24df94b.shtml",
            ]
    
    
    for u in url:
        site = get_site(u)
        print site
        
        try:
            parser = getattr(sys.modules[__name__], "parse_url_%s_%s" % (site, "video"))
            print site,": ",json.dumps(parser(u, site))
        except Exception, e:
            print "exception: %s" % e

