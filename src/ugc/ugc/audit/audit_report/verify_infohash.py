#!/usr/bin/python
# -*- coding:utf-8 -*-

#store ip:port/api/?cmd=upload_data&cli=upload_verify_data report data.
import json

class VerifyFiles(object):
    funshion_id = ""
    tid = ""

    def  __init__(self):
        pass

class VerifyInfoHash(object):
    info_hash = ""
    file_list = []

    def parse_files(self, files_json):
        try:
            self.file_list = []
            for item in files_json:
                verifyfile = VerifyFiles()
                verifyfile.funshion_id = item['funshion_id']
                verifyfile.tid = item['tid']
                #self.file_list.append(verifyfile)
                file_list.append(verifyfile)
            return True
        except Exception,e:
            print e
            return False

    def serialization(self, json_info):
        try:
            if json_info == None:
                print 'the json_info is none.'
                return False
            self.info_hash = json_info['infohash']
            json_files = json_info['files']
            #self.parse_files(json_files)
            #print self.file_list
            if not self.parse_files(json_files):
                return False
            return True
        except Exception,e:
            print e
            return False


if __name__ == "__main__":

     verify_infohash = "{\"infohash\":\"11111\",\"files\":[{\"funshion_id\":\"aaa\",\"tid\":\"tid1\"},{\"funshion_id\":\"bbb\", \"tid\":\"tid2\"},{\"funshion_id\":\"cccc\",\"tid\":\"3333\"}]}"
     try:
        info_hash = VerifyInfoHash()
        json_str = json.loads(verify_infohash)
        info_hash.serialization(json_str)
        print 'outsize: '
        print 'infohash:', info_hash.info_hash
        for item in info_hash.file_list:
            print item.funshion_id, item.tid
        print 'finish.'
     except Exception,e:
        print e
