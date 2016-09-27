#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import re
import json
import urllib2
import urllib
from django.http import HttpResponse

def parse_one_url(url):

    if not check_scheme(url):
        return None

    #parse
    site = get_site(url)
    try:
        parser = getattr(sys.modules[__name__], "parse_url_%s" % site)
    except Exception, e:
        return None
    ret = None
    try:
        ret = parser(url)
    except Exception, e:
        return None

    return ret
    
def parse_url(request):
    url = request.GET.get("url")
    #check scheme
    if not check_scheme(url):
        return HttpResponse('{"tips": u"非http/https地址"}')

    #parse
    site = get_site(url)
    try:
        parser = getattr(sys.modules[__name__], "parse_url_%s" % site)
    except Exception, e:
        return HttpResponse('{"tips": u"不支网站: %s"}' % site)

    try:
        ret = parser(url)
    except Exception, e:
        return HttpResponse('{"tips": u"无法解析url"}')

    return HttpResponse(json.dumps(ret))

def check_scheme(url):
    return url[:4] == "http"

def get_site(url):
    r = re.compile('^.*://\w+\.(\w+).\w+/.*$')
    m = r.match(url)
    if m:
        return m.group(1)
    return ""

def parse_url_base(url, pattern):
    res = {"tips":u" ", "title": u" ", "tag": u" ", "description":u" ", "channel": u" "}
    _opener = urllib2.build_opener()
    _opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36')]
    response = _opener.open(url, timeout = 30)
    if response.getcode() == 200:
        content = response.read()
        response.close()

        for (k, v) in pattern.items():
            for r in v:
                m = r.findall(content)
                if m:
                    #res[k] = "|".join(m)
                    res[k] = m[0]
                    if not res[k]:
                        res[k] = u" "
                    break
                res[k] = u" "
    return res

def parse_url_youku(url):
    pattern = {'title': [re.compile(r'<span id="subtitle">(.*?)</span>', re.S), re.compile(r'<h1 class="title".*?>(.*?)</h1>', re.S)], 'tag': [re.compile(r'var tags="(.*?)";', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<div class="crumbs">.*?<a.*?>(.*?)</a>.*?</div>', re.S)]}
    ret = parse_url_base(url, pattern)

    if ret and ret['tag']:
        ret['tag'] = urllib.unquote(ret['tag'].encode('utf8')).decode('utf8').rstrip('|')
    return ret

def parse_url_tudou(url):
    pattern = {'title': [re.compile(r'<h1 class="kw".*>(.*?)</h1>', re.S)], 'tag': [re.compile(r"tag: '(.*?)'", re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="v_channel">.*?<a.*?>(.*?)</a>.*?</span>', re.S)]}
    ret = parse_url_base(url, pattern)

    for k, v in ret.items():
        ret[k] = v.decode('utf8')

    if ret and ret['tag']:
        ret['tag'] = ret['tag'].replace(',', '|')

    return ret

def parse_url_56(url):
    pattern = {'title': [re.compile(r'<span id="vh_title_text".*?>(.*?)</span>', re.S), re.compile(r'<h1 id="video_title_text".*>(.*?)</h1>', re.S)], 'tag': [re.compile(r'"tags":"(.*?)"', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="crumbs">.*?<a .*?>.*?</a>.*?<a .*?>(.*?)</a>.*?</span>', re.S), re.compile(r'<span class="crumb">.*?<a .*?>.*?</a>.*?<a .*?>(.*?)</a>.*?</span>', re.S)]}
    ret = parse_url_base(url, pattern)

    #decode
    if ret and ret['tag']:
        ret['tag'] = ret['tag'].decode('unicode-escape').replace(',', '|')

    return ret

def parse_url_ku6(url):
    pattern = {'title': [re.compile(r'title: "(.*?)"', re.S)], 'tag': [re.compile(r'tag: "(.*?)"', re.S)], 'description': [re.compile(r'<meta name="description" content="(.*?)"', re.S)], 'channel': [re.compile(r'<span class="ckl_chane">.*?<a .*?>(.*?)</a>.*?</span>', re.S)]}
    ret = parse_url_base(url, pattern)

    #decode
    if ret and ret['title']:
        ret['title'] = ret['title'].decode('unicode-escape')
    if ret and ret['tag']:
        ret['tag'] = ret['tag'].decode('unicode-escape').replace(' ', '|').rstrip('|')
    if ret and ret['description']:
        ret['description'] = ret['description'].decode('gbk')
    if ret and ret['channel']:
        ret['channel'] = ret['channel'].decode('gbk')

    return ret

if __name__ == "__main__":
    url1 = ["http://v.youku.com/v_show/id_XNzIzNzYwMjY4.html", 
            "http://www.tudou.com/programs/view/g3SZOD8p-ss/?FR=LIAN", 
            "http://www.56.com/u96/v_MTE4MTgxMjY5.html", 
            "http://www.56.com/u63/v_MTIwMzg3OTI0.html", 
            "http://v.ku6.com/show/Ujby2SQ8pl9_FqgR1TB0Sg...html?hpsrc=1_24_1_1_0"]

    url2 = ["https://v.youku.com/v_show/id_XNzIzNzYwMjY4.html", 
            "www.tudou.com/programs/view/g3SZOD8p-ss/?FR=LIAN", 
            "http://www.5656.com/u96/v_MTE4MTgxMjY5.html", 
            "ftp://v.ku6.com/show/Ujby2SQ8pl9_FqgR1TB0Sg...html?hpsrc=1_24_1_1_0"]
    
    '''
    print map(check_scheme, url1)
    print map(check_scheme, url2)
    print map(get_site, url1)
    print map(get_site, url2)
    '''
    for u in url1:
        site = get_site(u)
        try:
            parser = getattr(sys.modules[__name__], "parse_url_%s" % site)
            print json.dumps(parser(u))
        except Exception, e:
            print "exception: %s" % e

