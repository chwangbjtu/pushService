#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import Queue
#import task_queue
import constant

import verify_data_mgr  
import verify_infohash_mgr
import verify_ms_info_mgr

class HttpBusiness:
    '''add vid2 and get the download vid2  and the vid1
    '''
    def __init__(self):
        self._verify_videodata = verify_data_mgr.VerifyDataMgr.instance()
        self._verify_infohash = verify_infohash_mgr.VerifyInfohashMgr.instance()
        self._verify_ms_info = verify_ms_info_mgr.VerifyMsInfoMgr.instance()

    def add_transcode_info(self, transcodeinfo):
        try:
            if transcodeinfo != None:
                verify_data_json = json.loads(transcodeinfo)
                #can add some filter info.

                #process
                (code, res) = self._verify_videodata.process(verify_data_json)
                print 'add_transcode_info ', code, res
                if code != constant.SUCCESS:
                    print code, res
                    return constant.FAIL
                return constant.SUCCESS
            else:
                return constant.FAIL
        except Exception, e:
            print e
            return constant.FAIL


    def add_package_info(self, pack_info):
        try:
            if pack_info != None:
                verify_hash_json = json.loads(pack_info)
                #can add some filter info.
                #process
                (code, res) = self._verify_infohash.process(verify_hash_json)
                print 'add_package_info ', code, res
                if code != constant.SUCCESS:
                    print code, res
                    return constant.FAIL
                return constant.SUCCESS
            else:
                return constant.FAIL
        except Exception, e:
            print e
            return constant.FAIL

    def add_video_loaded_info(self, loaded_info):
        """handle crane's last report, record ms load dat file addr"""
        try:
            if loaded_info != None:
                verify_ms_json = json.loads(loaded_info)
                (code, res) = self._verify_ms_info.process(verify_ms_json)
                print 'add_video_loaded_info ', code, res
                if code != constant.SUCCESS:
                    return constant.FAIL
                return constant.SUCCESS
            else:
                return constant.FAIL
        except Exception, e:
            print e
            return constant.FAIL

def __test():
    hs = HttpBusiness()
    print hs.add_task("XNDc5NDQzOTU1")      
    print hs.get_video_task()   
    print hs.get_vp_task()    
    print "--------------------------------------------------------"
    
if __name__ == "__main__":   
    __test()
    import os
    os.system("PAUSE")

