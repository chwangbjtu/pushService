import urllib
from urllib import quote
import urllib2
import sys
import json
import logging
import logging.handlers
import os
import time
import etc
import downloader
import visitor
import youku_urls
import joinfile
import tlogger
import file_cat
import parse

def logger_init1():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
        
    handler = logging.handlers.RotatingFileHandler(
                  "./" + "worker.log", mode='a', maxBytes=1024*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)
        
    logger.addHandler(handler)
    logger.info("start log")

def main():
    logger_init1()
    tvisitor = visitor.visitor()
    site = None
    task_id = None
    vid = None
    src_url = None
    ret = None
    sites = json.loads(etc.sites)
    other_sites = json.loads(etc.other_sites)
    #jsites = json.loads(sites)
    (task_id,vid,site,src_url) = tlogger.tlogger.instance().getlog()
    first = True
    filecat = file_cat.file_cat()
    while True:
        
        try:
            if first and task_id != None and site != None and vid != None and src_url != None:
                first = False
            else:
                (task_id,site,vid,src_url) = tvisitor.get_msg()
            if site == None or task_id == None or vid == None or src_url == None:
                time.sleep(10)
                logging.error("task_id or site or vid or src_url is null")
                continue

            logging.info("task_id is %s,site is %s,vid is %s",task_id,site,vid)
            tlogger.tlogger.instance().writelog(task_id,vid,site,src_url)
            res = 1
            #if site == "yk":
            if site in sites:
                for i in range(etc.retry_num):
                    encode_url = quote(src_url)
                    res = download1(site,vid,encode_url)
                    if res == 0:
                        break
            elif site in other_sites:
                for i in range(etc.retry_num):
                    res = download2(site,vid)
                    if res == 0:
                        break
            else:
                logging.error("site : %s not in sites",site)
            
            if res != 0:
                ret = "1"
            else:
                ret = "0"
        except Exception, err:
            logging.error("" + str(err))
            time.sleep(1)
            ret = "1"
        logging.info("task_id is:" + str(task_id) +" ,site is " + str(site) + ",vid is :"  + str(vid)  + "ret is:" + str(ret))
        tvisitor.update_task(site,task_id,vid,ret)
        logging.info("task_id is:" + str(task_id) +" ,site is " + str(site) + ",vid is :"  + str(vid)  + "ret is:" + str(ret))
        #exit(1)

def get_formatCode(real_url):
    format = None
    try:
        url = "http://vpwind.flvcd.com/parse-fun.php?format=real&url="  + real_url
        f = urllib2.urlopen(url)
        res =  f.read()
        rjson = json.loads(res)
        if "formatCodeList" in rjson:
            formatCodeList = rjson["formatCodeList"].split("|")
            tlen = len(formatCodeList)
            if tlen > 0:
                format = formatCodeList[tlen-1]
                logging.info("url:" + str(real_url) + " , format is : " + str(format))
    except Exception, err:
        logging.error("get_formatCode error: site:"+ site + ",vid:" + vid)
        logging.error("get_formatCode error:" + str(err))
        
    return format

def get_last_download_url(url,index):
    down_url = None
    try:
        f = urllib2.urlopen(url)
        res =  f.read()
        rjson = json.loads(res)
        rurl = None
        type = ""
        if "TYPE" in rjson:
            type = rjson["TYPE"]
        urllist = []

        if "error" not in rjson:
            res_urls = rjson["V"]
            if type == "DIRECT":
                for i in range(len(res_urls)):
                    urllist.append(res_urls[i]["U"])
            elif type == "CUSTOM":
                turllist = []
                for i in range(len(res_urls)):
                    url = res_urls[i]["C"]
                    tf = urllib2.urlopen(url)
                    tres = tf.read()
                    tjson = json.loads(tres)
                    rurl = tjson['l']
                    urllist.append(rurl)
        if index < len(urllist):
            down_url = urllist[index]
    except Exception, err:
        logging.error("get last donwload url error," + str(url) + "," + str(i))
        logging.error("get last donwload url error :" + str(err))
        down_url = None
    return down_url

def download1(site,vid,real_url):
    res = 1
    try:
        #http://v.youku.com/v_show/id_XNTQxNTU2MDQw.html
        headurl = ""
        sites = json.loads(etc.sites)
        if site in sites:
            #headurl = headurl + sites[site]
            #headurl = headurl + vid + ".html"
            headurl = real_url
        format = get_formatCode(real_url)
        if not format:
            return res

        #url = "http://vpwind.flvcd.com/parse-fun.php?format=real&url="  + headurl
        url = "http://vpwind.flvcd.com/parse-fun.php?format=" + str(format) + "&url="  + headurl
        f = urllib2.urlopen(url)
        res =  f.read()
        #logging.info("parse json:" + str(res))
        rjson = json.loads(res)
        #logging.info("parse json:" + str(res))
        rurl = None
        type = ""
        if "TYPE" in rjson:
            type = rjson["TYPE"]
        urllist = []

        if "error" not in rjson:
            res_urls = rjson["V"]
            if type == "DIRECT":
                for i in range(len(res_urls)):
                    urllist.append(res_urls[i]["U"])
            elif type == "CUSTOM":
                turllist = []
                for i in range(len(res_urls)):
                    curl = res_urls[i]["C"]
                    tf = urllib2.urlopen(curl)
                    tres = tf.read()
                    tjson = json.loads(tres)
                    rurl = tjson['l']
                    urllist.append(rurl)
        #download
        if len(urllist) == 0:
            res = 1
            return res
        elif len(urllist) == 1:
            filename = etc.data_path + vid
            res = downloader.download(site,vid,urllist[0],filename)
        else:
            filelist = []
            for i in range(len(urllist)):
                filename = etc.data_path + vid + "_" + str(i)
                filelist.append(filename)
                try:
                    tdurl = get_last_download_url(url,i)
                    if tdurl:
                        res = downloader.download(site,vid,tdurl,filename)
                    else:
                        logging.error("get_last_download_url error," + str(url) +"," + str(i))
                except Exception, err:
                    logging.error("download err: %s" , str(err))
                if res != 0:
                    logging.error("download error: site : %s ,vid %s" ,  str(site),str(id))
                    return res
            #concat
            filenum = len(urllist)
            targetfile = etc.data_path + str(vid)
            filecat = file_cat.file_cat()
            try:
                res = filecat.cat_file(site,filelist,targetfile)
            except Exception, err:
                logging.error("cat file error %s,%s",str(site),str(id))
            filelen = len(filelist)
            for i in range(filelen):
                if os.path.exists(filelist[i]):
                    os.remove(filelist[i])
    except Exception, err:
        logging.error("download error: site:"+ site + ",vid:" + vid)
        logging.error("download error:" + str(err))
        res = 1
    return res
            
def download2(site,id):
    res = 1
    try:
        jinfo = {}
        jinfo["site"] = str(site)
        jinfo["vid"] = str(id)
        info = json.dumps(jinfo)
        #info = (site,id)
        #download
        urls = parse.get_video_url(info)
        filelist = []
        if urls:
            url_num = len(urls)
            filename = str(id)
            if url_num > 0:
                for i in range(url_num):
                    filename = etc.data_path + str(id) + str(i)
                    res = 1
                    try:
                        res = downloader.download(site,id,urls[i],filename)
                        filelist.append(filename)
                    except Exception, err:
                        logging.error("download err: %s" , str(err))
                    if res != 0:
                        logging.error("download error: site : %s ,vid %s" ,  str(site),str(id))
            filenum = len(urls)
            #catfiles
            targetfile = etc.data_path + str(id)
            filecat = file_cat.file_cat()
            try:
                res = filecat.cat_file(site,filelist,targetfile)
            except Exception, err:
                logging.error("cat file error %s,%s",str(site),str(id))
            filelen = len(filelist)
            for i in range(filelen):
                if os.path.exists(filelist[i]):
                    os.remove(filelist[i])
            '''
            joinmodel = joinfile.joinfile()
            filelist = [] 
            if filenum > 0:
                res = 0
                for j in range (filenum):
                    filename = etc.data_path + str(id) + str(j)
                    filelist.append(filename)
                targetfile = etc.data_path + str(id)
            joinmodel.concat_file(str(id),filelist, targetfile)
            if res == 0:
                j = 0
                for j in range (filenum):
                    filename = etc.data_path + str(id) + str(j)
                    try:
                        os.remove(filename)
                        pass
                    except Exception, err:
                        logging.error("remove file error,filename %s",filename)
            '''
                
    except Exception, err:
        logging.error("download error: site:"+ site + ",vid:" + id)
        logging.error("download error:" + str(err))
        res = 1
    return res

def downloadn(site,task_id):
    res = 1
    try:
        (urls,type) = youku_urls.get_urls(task_id)
        if not urls:
            return res
        len1 = len(urls)
        if len1 <= 0:
            return res
        joinmodel = joinfile.joinfile()
        filelist = [] 
        res = 0
        for j in range (len1):
            filename = etc.data_path + task_id + "__" + str(j)
            filelist.append(filename)
            res = downloader.download(site,task_id,urls[j],filename)
            if res != 0:
                raise Exception()
        targetfile = etc.data_path + task_id
        joinmodel.concat_file(task_id,filelist, targetfile)
        
    except Exception, err:
        logging.error("download error:" + str(err))
        res = 1
        return res
    finally:
        try:
            if len(filelist) != 0:
                filenum = len(filelist)
                for k in range(filenum):
                    try:
                        os.remove(filelist[k])
                    except Exception, err:
                        logging.error("1remove tmpfile error:" + str(err))
        except Exception, err:
            logging.error("remove tmpfile error:" + str(err))
            res = 1
        return res

            

if __name__ == "__main__":
    main()

