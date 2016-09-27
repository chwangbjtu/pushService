#!/usr/bin/python
# -*- coding:utf-8 -*- 

#__all__ = ['get_downloadurls', 'file_type_of_url']

import urllib
import json
from random import randint
from time import time
import re
import sys
import os.path
import getopt
import threading
import urllib2_thread_wrapper
import string
import logging
import logging.handlers

def file_type_of_url(url):
    return str(re.search(r'/st/([^/]+)/', url).group(1))

def logger_init():
    if os.path.isfile("./videoparsek.log"):
        return None
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
                  "./" + "videoparsek.log", mode='a', maxBytes=1024*1024*50, backupCount=5)
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logging.info("start log")

def find_videourls(jsoninfo, stream_type=None):
    try:
        testu = utilC()
        strna = testu.funna(jsoninfo["ep"])
        videotype = ""
        videoinfo = jsoninfo["streamfileids"]#get videotype:flv/mp4/hd2...
        videoinfo = jsoninfo["streamfileids"]#get videotype:flv/mp4/hd2...

        tq = {"flv":"flv","mp4":"mp4","hd2":"flv","3gphd":"mp4","3gp":"flv"}
        #types = ("mp4","flv","hd2","3gp")
        types = ("flv","hd2","3gp")
        typeslen = len(types)        

        if len(videoinfo) > 0:
            for i in range(0,typeslen):
                if types[i] in videoinfo:
                    videotype = str(types[i])
                    break
            #for key in videoinfo:
            #    tvalue = videoinfo[key]
            #    if len(tvalue) != 0:
            #        videotype = str(key)
            #        break

        para = (19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26)
        strf = testu.funF("b4eto0b4",para)
        stre = testu.funE(strf,strna)
        sid = stre.split("_")[0]
        token = stre.split("_")[1]
        stotal_time = str(jsoninfo["seconds"])
        total_timelist = stotal_time.split(".")
        total_time = int(total_timelist[0])
        testt = utilT(jsoninfo,videotype,sid,token)
        ttotal_time = testt.get_total_time()
        if total_time - ttotal_time >=total_time/2 or ttotal_time-total_time >= total_time/2:
            logging.warning("videotime is not match")
            info = json.dumps(jsoninfo)
            logging.warning(info)
            #return (None,None)
        urls = []
        urls = testt.get_urls()
        if len(urls) > 0:
            for i in range(0,len(urls)):
                logging.info("url:" + urls[i] + "," + str(videotype))
            return (urls,videotype)
    except Exception,e:
        logging.error("find_videourls error" + str(e))
        return (None,None)

    logging.warning("return none,none")
    return (None,None)

def ungzip(data):
    import StringIO
    compressed_stream = StringIO.StringIO(data)
    import gzip
    gzipper = gzip.GzipFile(fileobj=compressed_stream)
    return gzipper.read()

def deflate(data):
    #todo : implement this functhion
    return data

def undeflate(data):
    return data

def get_json_from_ids(videoid2):
    try:
        content = None
        opener = urllib2_thread_wrapper.get_opener()
        response = opener.open('http://v.youku.com/player/getPlayList/VideoIDS/' + videoid2, timeout = 30)
        content = response.read()
        if response.info().get('Content-Encoding') == 'gzip':
            content = ungzip(content)
        elif response.info().get('Content-Encoding') == 'deflate':
            content = undeflate(content)    
    except Exception,e:
        logging.error(str(e) + "," + str(videoid2))
        return None

    firstjson = None
    firstjson = json.loads(content)
    logging.debug("first http resp:" + str(content) + ",vid:" + str(videoid2))
    try:
        content1 = None
        videoid = None
        videoid = firstjson["data"][0]["videoid"]
        opener1 = urllib2_thread_wrapper.get_opener()
        response1 = opener.open('http://v.youku.com/player/getPlayList/VideoIDS/' + str(videoid) + "/Pf/4/ctype/12/ev/1/Type/Folder/Fid/22327221", timeout = 30)
        content1 = response1.read()
        if response1.info().get('Content-Encoding') == 'gzip':
            content1 = ungzip(content)
        elif response1.info().get('Content-Encoding') == 'deflate':
            content1 = undeflate(content1)    
    except Exception,e:
        logging.error(str(e) + "," + str(videoid2))
        return None

    content2 = ""

    secondjson = json.loads(content1)
    logging.debug("second http resp:" + str(content1))
    try:
        videoinfo = None
        if len(secondjson["data"]) >= 1:
            videoinfo = secondjson["data"][0]["segs"]
        types = ("mp4","flv","hd2","3gp")
        typeslen = len(types)    
        if videoinfo:
            for i in range(0,typeslen):
                if types[i] in videoinfo:
                    videotype = str(types[i])
                    break

        lengthsegstype = len(secondjson["data"][0]["segs"][videotype])
        for i in range(0,lengthsegstype):
            if secondjson["data"][0]["segs"][videotype][i]["k"] == -1:
                secondjson["data"][0]["segs"][videotype] = firstjson["data"][0]["segs"][videotype]

    except Exception,e:
        logging.error(str(e) + "," + str(videoid2))
        return None

    content2 = json.dumps(secondjson)
    logging.debug("check end second json is:" + str(content2) )

    return content2

def get_downloadurl_from_json(jsoninfo):
    try:
        jsoninfo = json.loads(jsoninfo)
        injson = jsoninfo["data"][0]
        return find_videourls(injson,None)
    except:
        return (None,None)
        

########################################################
####base functions
##utilC
class utilC:

    def funE(self,a,c):
        q = 0

        b = {}
        f = 0
        h = 0
        length = len(a)
        while h<256:
            b[h] = h
            h = h+1

        i = 0
        h = 0
        while h<256:
            tmp = int(ord(a[h%length]))
            tf = ( f + b[h] + tmp)%256
            f = tf
            i = b[h]
            b[h] = b[f]
            b[f] = i
            h = h +1

        q=0
        f=0
        h=0
        length = len(c)
        e = ""

        q=0
        while q<length:
            h = (h+1)%256
            f = (f+b[h])%256
            i = b[h]
            b[h] = b[f]
            b[f] = i
            tmp1 = chr((ord(c[q])) ^ b[(b[h] + b[f]) %256 ]);
            e = e + tmp1
            q = q + 1

        return e

    def funF(self,a,c):
        length1 = len(a)
        f = 0
        b = {}
        while f<length1 :
            i = 0
            if ( a[f] >= 'a' and a[f] <= 'z'):
                tmp = int(ord(a[f])) - 97
            else:
                tmp = int(a[f])+26

            i = tmp
            
            e = 0
            tmpi = 0
            while e<36 :
                if c[e] == i:
                    i = e
                    break
                e = e+1
            if i > 25:
                b[f] = i-26
            else:
                b[f] = chr(i+97)
            f = f+1
            
        res = ""
        for key in b:
            res = res + str(b[key])
        return res

    def funna(self,info1):
        info = str(info1)
        res = ""
        length = len(info)
        q = 0
        while q < length:
            q = q +1
        if length == 0:
            return res;

        listh = [ - 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1]

        i = 0
        while i < length:
            #first do while
            tmpi = listh[int(ord(info[i])) & 255]#
            i = i+1
            while i < length and -1 == int(tmpi):
                index = listh[int(ord(info[i])) & 255]
                i = i+1

            if -1 == int(tmpi):
                break

            #second do while
            tmpi2 = listh[int(ord(info[i])) & 255]
            i = i+1
            while i < length and -1 == int(tmpi2):
                tmpi2 = listh[int(ord(info[i])) & 255]
                i = i+1

            if -1 == int(tmpi):
                break

            res1 = chr(tmpi<<2 | (tmpi2&48) >> 4)
            res = res + res1

            #third do while
            tmpi = int(ord(info[i])) & 255
            i = i+1
            if tmpi == 61:
                return res
            tmps = listh[tmpi]
            tmpi = tmps

            while i< length and -1 == int(tmpi):
                tmpi = int(ord(info[i])) & 255 
                i = i+1 
                if tmpi == 61: 
                    return res
                tmps = listh[tmpi]
                tmpi = tmps

            if -1 == int(tmpi):
                break

            res1 = chr((tmpi2&15)<<4|(tmpi&60)>>2)
            res = res + res1
            
            #four do while
            tmpi2 = int(ord(info[i])) & 255
            i = i+1
            if tmpi2 == 61:
                return res
            tmps = listh[tmpi2]
            tmpi2 = tmps

            while i< length and -1 == int(tmpi2):
                tmpi2 = int(ord(info[i])) & 255
                i = i+1
                if tmpi2 == 61:
                    return res
                tmps = listh[tmpi2]
                tmpi2 = tmps

            if -1 == int(tmpi2):
                break

            res1 = chr((tmpi&3)<<6|tmpi2)
            res = res + res1

        return res


    def funD(self,info1):
        info = str(info1)
        res = ""
        length = len(info)
        conststr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        if length == 0:
            return res;
        
        i = 0
        while i < length:
            tmp1 = int(ord(info[i])) & 255#
            i = i + 1
            if i == length:
                res1 = res + conststr[tmp1>>2]
                res2 = res1 + conststr[(tmp1&3)<<4]
                res = res2 + "=="
                break
            tmp2 = int(ord(info[i]))
            i = i + 1
            if i == length:
                res1 = res + conststr[tmp1>>2]
                res2 = res1 + conststr[(tmp1&3)<<4 | (tmp2&240)>>4]
                res3 = res2 + conststr[(tmp2&15)<<2]
                res = res3 + "="
                break

            tmp3 = int(ord(info[i]))
            i = i + 1
            res1 = res + conststr[tmp1>>2]
            res2 = res1 + conststr[(tmp1&3)<<4 | (tmp2&240)>>4]
            res3 = res2 + conststr[(tmp2&15)<<2 |(tmp3&192)>>6]
            res = res3 + conststr[tmp3&63]

        return res

##utilU
class utilU:
    _randomSeed = 0
    _cgStr = ""

    def __init__(self,seed):
        self._randomSeed = seed
        self.cg_hun()

    def cg_hun(self):
        a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\:._-1234567890"
        
        c = len(a)
        b = 0
        while b < c:
            f = int(self.ran()*len(a))
            self._cgStr = self._cgStr + a[f]
            tmp = a[f]
            tmp1 = a.split(tmp)
            len1 = len(tmp1)
            str1 = ""
            for i in range(0,len1):
                str1 = str1 + tmp1[i]
                i = i + 1

            a = str1
            b = b + 1

        return str1

    def ran(self):
        tmp = (211*self._randomSeed + 30031) % 65536
        self._randomSeed = tmp
        return self._randomSeed/float(65536)

    def cg_fun(self,a):
        ta = a.split("*")
        c = ""
        length = len(ta)
        b = 0
        while b < length and len(ta[b]) != 0:
            index = int(string.atoi(ta[b]))
            c = c + self._cgStr[index]
            b = b + 1
        return c

##utilT
class utilT:
    _sid = ""
    _seed = ""
    _fileType = "flv"
    _b = None
    _streamFileIds = None
    _urllist = []
    _totaltime = 0

    def __init__(self,a,c,sid,token):#json,type
        self._sid = ""
        self._seed = ""
        self._fileType = "flv"
        self._b = None
        self._streamFileIds = None
        self._urllist = []
        self._totaltime = 0


        self._seed = a["seed"]
        self._fileType = c
        self._sid = sid
        self._token = token
        self._totaltime = 0
        b = utilU(self._seed)
        json.dumps(a["segs"])

        if c in a["segs"]:
            f = ()
            i = 0
            g = 0
            length = len(a["segs"][c])
            while g < length:
                try:
                    h = a["segs"][c][g]
                    self._totaltime = self._totaltime + int(h["seconds"])
                    fileid = self.getFileId(a["streamfileids"],c,int(g),b)
                    turl = self.getVideoSrc(h["no"],a,c,fileid)
                    if len(turl) > 0:
                        logging.info("fileid:" + str(fileid) + "," + str(turl) + str(g))
                        self._urllist.append(turl)
                    else:
                        logging.info("get url is empty")
                    g = g + 1
                except Exception,e:
                    g = g + 1
                    logging.error("" + str(e))


    def get_urls(self):
        return self._urllist

    def get_total_time(self):
        return self._totaltime

    def getFileId(self,a,c,b,f):
        streamFid = ""
        for i in a:
            if (i==c):
                streamFid = a[i]
                break

        if len(streamFid) == 0:
            return ""
        c = f.cg_fun(streamFid)
        a = ""
        clen = 8
        if len(c) < 8:
            clen = len(c)
        for i in range(0,clen):
            a = a + c[i]

        b1 = str(hex(int(b)))
        b1 = b1.upper()
        b = ""
        lengthb = len(b1)
        if lengthb <3:
            b = "0"
        else:
            for i in range(2,lengthb):
                b = b + b1[i]

        if 1 == len(b):
            b = "0" + b
        b = b.upper()
        tc = c
        length = len(tc)
        c = ""
        if length < 10:
            return a + b
        for i in range(10,length):
            c = c + tc[i]
        ddd = a+b+c
        return a+b+c
        

    def getVideoSrc(self,a,c,d,f):
        if len(c["videoid"]) == 0 or len(d) == 0:
            return ""
        th = {"flv":0,"flvhd":0,"mp4":1,"hd2":2,"3gphd":1,"3gp":0}
        h = th[d]
        tq = {"flv":"flv","mp4":"mp4","hd2":"flv","3gphd":"mp4","3gp":"flv"}
        q = tq[d]
        k = ""
        ksid = str(hex(int(a)))
        if len(ksid) < 3:
            k = "0"
        else:
            for i in range(2,len(ksid)):
                k = k + ksid[i]
        
        a = int(a)
        l = c["segs"][d][a]["seconds"]
        if 1==len(k):
            k = "0" + k

        a = str(c["segs"][d][a]["k"])
        if len(a) == 0:
            a = c.key2+c.key1

        ip = str(c["ip"])
        c =  "/player/getFlvPath/sid/" + self._sid + "_" + k + "/st/" + str(q) + "/fileid/" + str(f) + "?K=" + str(a) + "&hd=" + str(h) + "&myp=0&ts=" + str(l) + "&ypp=0"
        
        tlist = (19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26)
        tu = utilC()
        tf = tu.funF("boa4poz1",tlist)
        tparae = self._sid + "_" + f + "_" + self._token
        te = tu.funE(tf,tparae)
        
        td = tu.funD(te)
        tlib = urllib.urlencode({'name':td})
        tliblist = tlib.split("=")

        c = c + "&ep=" + tliblist[1] + "&ctype=12&ev=1" + "&token=" + self._token

        url = "http://k.youku.com" + c + "&oip=" + ip
        return url
       
def get_urls(id):
    urls = None
    type = None
    try:
        info = get_json_from_ids(id)
        (urls,type) = get_downloadurl_from_json(info)
    except Exception, err:
        logging.error("get urls error:" + str(err))
        urls = None
        type = None

    return (urls,type)

if __name__ == "__main__":
    #id = "XNzI3ODg5NTAw"
    id = "XNzI3NzU2Njcy"
    id = "XNzI3ODg5NTAw"
    id = "XMzA2MTM3Mjg4"
    id = "XNzUwODI3NDEy"
    id = "XNzM0NDA0NTYw"
    id = "XNzUwNTQyNDEy"
    id = "XNzU4NzM0NDQ4"
    id = "XNzYxNjIwNjYw"
    id = "XNTE0NTQ0ODU2"
    id = "XNzgzOTQxODYw"
    id = "XNzk2NTM5NTQw"
    #id = "XNjI4NDkxMDk2"
    id = "XNjI0NTMwNTQ0"
    #info = get_json_from_ids(id)
    #print get_downloadurl_from_json(info)
    urls = get_urls(id)
    print urls
