#!/usr/bin/python
# -*- coding:utf-8 -*-

#store ip:port/api/?cmd=upload_data&cli=upload_verify_data report data.
import json
import re

class FunshionInfo(object):
    funshion_id = ""
    rate = ""
    #image_url = ""
    large_image = ""
    small_image = ""
    video_url = ""
    filename = ""
    filesize = 0
    milliseconds = 0

    def  __init__(self):
        pass

class AuditVerifyData(object):
    tid = ""
    state = ""
    ip = ""
    port = ""
    funshion_list = {}

    def __init__(self):
       pass

    def build_image(self, funshion, image_url):
       try:
           small_img_str = ""
           large_img_str = ""
           for img_item in image_url:
               #print img_item
               flag = re.search(".*_\d.jpg",img_item)
               if flag:
                  #print 'small image'
                  small_img_str += "%s |" % (img_item)
               else:
                  #print 'large image'
                  large_img_str = img_item
           funshion.small_image = small_img_str
           funshion.large_image = large_img_str
           #large_image
           return True
       except Exception,e:
           print e
           return False

    def parse_funshion(self, funshion_info):
        try:
            for item in funshion_info:
                funshion = FunshionInfo()
                funshion.funshion_id = item['funshion_id']
                funshion.rate = item['rate']
                #funshion.image_url = self.build_image(item['img_url'])
                self.build_image(funshion, item['img_url'])
                funshion.video_url = item['video_url']
                funshion.filename = item['filename']
                funshion.filesize = item['size']
                funshion.milliseconds = item['milliseconds']
                self.funshion_list[funshion.rate] = funshion
                print 'rate: ', funshion.rate, ', small_image:', funshion.small_image, ', large_image:', funshion.large_image
            return True
        except Exception,e:
            print e
            return False

    def serialization(self, json_info):
        try:
            if json_info == None:
                print 'the json_info is none.'
                return False
            self.tid = json_info['tid']
            self.state = json_info['state']
            self.ip = json_info['ip']
            self.port = json_info['port']
            self.info_list = json_info['info']
            #print 'serial: ', self.tid, self.state, self.ip, self.port
            #print self.info_list
            if self.state == "fail":
                print 'verify AuditVerifyData state fail'
            else:
                self.parse_funshion(self.info_list)
            return True
        except Exception,e:
            print e
            return False


   #for client test.
if __name__ == "__main__":
    verify_data = "{\"tid\":\"323123\",\"state\":\"success\",\"ip\":\"192.168.135.13\",\"port\":\"8100\", \
    \"info\":[{ \"funshion_id\":\"fsdid\", \"rate\":\"biaoqing\",\"img_url\":[\"XXX1.jpg\",\"XXX2_1.jpg\",\"XXX3_2.jpg\",\"XXX4_3.jpg\",\"XXX5_4.jpg\",\"XXX6_5.jpg\",\"XXX7_6.jpg\"], \"video_url\":\"XXX\", \
            \"filename\":\"XXX\",\"size\":123,\"milliseconds\":111111},{ \"funshion_id\":\"fsdid2\", \"rate\":\"gaoqing\",\"img_url\":[\"XXX21.jpg\",\"XXX22_1.jpg\",\"XXX23_2.jpg\",\"XXX24_3.jpg\",\"XXX25_4.jpg\",\"XXX26_4.jpg\",\"XXX27_5.jpg\"], \"video_url\":\"XXX\", \
            \"filename\":\"XXX\",\"size\":456,\"milliseconds\":222222}]}"
    
    try:
        audit_data = AuditVerifyData()
        json_str = json.loads(verify_data)
        audit_data.serialization(json_str)
        print 'outsize: ',audit_data.tid, audit_data.ip,  audit_data.port
        fun_map = audit_data.funshion_list
        for key in fun_map:
            print key
            value = fun_map[key]
            print value.funshion_id, value.small_image, value.large_image, value.filename, value.filesize

        regex = ".*_\d.jpg"
        regexobject = re.compile(regex)
        img_url = "http://ugcimg.funshion.com:8089/2013_04_04/7be2e5bd5f0f456c1b8ad811a103963dffa9e004_9.jpg"
        flag = re.search(".*_\d.jpg",img_url)
        if flag:
            print 'small image'
        else:
            print 'large image'
        print 'finish.'
    except Exception,e:
        print e





