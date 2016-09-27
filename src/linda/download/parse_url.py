# -*- coding: utf-8 -*- 
import json
import re
import traceback
import base64
import urllib2
import urlparse
from urllib import urlencode
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
class HttpDownload(object):

    def __init__(self):
        self._opener = None
        self._opener = urllib2.build_opener()

    def get_data(self, url, ua=None, timeout=1):
        data = ''
        try:
            req = urllib2.Request(url)
            if ua:
                req.add_header('User-Agent', ua)
            resp =  self._opener.open(req, timeout=timeout)
            chunk_size = 100 * 1024
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                data += chunk
            resp.close()
        except HTTPError as e:
            print ('Error request [%s], code [%s]' % (url, e.code))
            #log.app_log.error('Error request [%s], code [%s]' % (url, e.code))
        except Exception, e:
            print "error"
            #log.app_log.error(traceback.format_exc())
        finally:
            #data = unicode(data,'utf-8')
            return data
    def post_data(self, url, body, ua=None,timeout=3):
        data = ''
        try:
            req = urllib2.Request(url)
            if ua:
                req.add_header('User-Agent', ua)
            resp =  self._opener.open(req, body, timeout=timeout)
            chunk_size = 100 * 1024
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                data += chunk
            resp.close()
        except HTTPError as e:
            log.app_log.error('Error request [%s], code [%s]' % (url, e.code))
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return data
class parse:
    def __init__(self):
        self.client = HttpDownload()
        self.format = ["original","super","high","normal","fluent"]
    def parse_url(self,url,retry=0):
        try:
            #decode url
            site = self.guess_site(url)
            if site == 'le':
                site = 'letv'
            if site == 'mgtv':
                site ='hunantv'
            return self.cracker_url(url,site,retry)
        except Exception,e:
            return []
    def cracker_url(self,url,site,retry):
        result = []
        try:
            #res = self.client.post_data("http://172.17.20.24/crack",json.dumps({"vid": "00000","url": url,"site":site,"os": "web","format":"all"}))
            res = self.client.post_data("http://172.17.20.24:7410/crack",json.dumps({"vid": "00000","url": url,"site":site,"os": "web","format":"all"}))
            #res = self.client.post_data("http://192.168.16.165:38888/crack",json.dumps({"vid": "00000","url": url,"site":site,"os": "web","format":"all"}))
            print res
            result = self.parse_video_info(res,site,retry)
            return result
        except Exception,e:
            #print traceback.format_exc()
            return result
    def parse_video_info(self,data,site,retry):
        result = []
        try:
            res = json.loads(data)
            type = res['type']
            start = res['start']
            end = res['end']
            formats = res['format']
            urls = res['seg']
            for item in self.format:
                if item in formats:
                    if type == '0':
                        #result = urls[item]
                        for i in urls[item]:
                            result.append(i.get('url'))
                        break
                    else:
                        result = self.parse_video_info_second(urls[item],start,end,site,retry)
                        break
            return result
        except Exception,e:
            #print traceback.format_exc() 
            return result
    def parse_video_info_second(self,urllist,start,end,site,retry):
        result = []
        try:
            for item in urllist:
                if site=='iqiyi' and retry==1:
                    tmp = item['url']+'&retry=1'
                    data = self.client.get_data(tmp)
                    data = data.decode()
                    url = data[data.find(start)+len(start):]
                    url = url[:url.find(end)]
                    result.append(url)
                else:
                    data = self.client.get_data(item['url'])
                    if site=='letv':
                        data = unicode(data,'utf-8')
                    if site=='iqiyi':
                        data = data.decode()
                    data = data.replace('\\','')
                    lens=data.find(start)
                    url = data[data.find(start)+len(start):]
                    url = url[:url.find(end)]
                    result.append(url)
            return result
        except Exception,e:
            return result
    def guess_site(self,url):
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
        except Exception as e:
            return ""
            #print traceback.format_exc()
            
if __name__=="__main__":
    test = parse()
    #res = test.parse_url("http://www.1905.com/vod/play/869029.shtml")
    #print "1905:",res
    #res = test.parse_url("http://v.youku.com/v_show/id_XMTQxOTIyNjg4OA==.html")
    #print "youku:",res
    #res = test.parse_url("http://www.56.com/w78/play_album-aid-14295959_vid-MTM5ODY4MzI0.html")
    #print "56:",res
    #res = test.parse_url("http://v.qq.com/cover/l/lgulqofu1vc0rme.html?vid=k0019yqzyi5")
    #print "qq:",res
    #res = test.parse_url("http://v.ku6.com/show/o82skl6Uenzs5y5S0T_TTg...html")
    #print "ku6:",res
    #res = test.parse_url("http://v.pptv.com/show/qaA9u3oX3RtibicGQ.html")
    #print "pptv:",res
    #res = test.parse_url("http://my.tv.sohu.com/pl/9088849/83956960.shtml",retry=1)
    #print res
    #res = test.parse_url("http://www.le.com/ptv/vplay/25093980.html")
    #print res
    #res = test.parse_url("http://www.letv.com/ptv/vplay/21768679.html")
    #print res
    #res = test.parse_url("http://v.ifeng.com/mil/mainland/201608/01f7342f-73cd-4472-8eed-2b050688b7d7.shtml")
    #print res
    #res = test.parse_url("http://www.mgtv.com/v/2/166217/c/3302185.html")
    #print res
    #res = test.parse_url("http://www.iqiyi.com/v_19rrl2q61o.html#vfrm=2-4-0-1")
    #print res
    res = test.parse_url("http://m.iqiyi.com/v_19rrmbr34s.html#vfrm=24-9-0-1")
    print res
    #res = test.parse_url("http://www.iqiyi.com/v_19rrl2n40w.html#vfrm=2-4-0-1")
    #print res
    #gamefy-iqiyi
    #res = test.parse_url("http://www.gamefy.cn/vplay.php?id=62201&class_id=13")
    #print res
    #gamefy-17173
    #res = test.parse_url("http://www.gamefy.cn/vplay.php?id=73404&class_id=12")
    #print res
    #gamefy-youku
    #res = test.parse_url("http://www.gamefy.cn/vplay.php?id=65949&class_id=12")
    #print res
    #gamefy-qq
    #res = test.parse_url("http://www.iqiyi.com/v_19rrlduzxo.html?fc=87451bff3f7d2f4a#vfrm=2-3-0-1")
    #print res
