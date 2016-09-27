#!/usr/bin/python
# -*- coding:utf-8 -*- 

import os
import logging
import logging.handlers
import time
import json
import etc
from flvjoin import *
from mp4join import *

READ_UNIT = 256 * 1024

if 'LD_LIBRARY_PATH' in os.environ:
    if os.environ['LD_LIBRARY_PATH'].find('./tools/ffmpeg/lib/:./tools/lib/') < 0:
        value = './tools/ffmpeg/lib/:./tools/lib/' + ':' + os.environ['LD_LIBRARY_PATH'] 
        os.environ['LD_LIBRARY_PATH'] = value
else:
    os.environ['LD_LIBRARY_PATH'] = './tools/ffmpeg/lib/:./tools/lib/'
print os.environ['LD_LIBRARY_PATH']

class file_cat:
    sites = json.loads(etc.special_flv)

    def cat_file(self,site,filelist,target_file):
        res = 0
        if not filelist or len(filelist) <= 1:
            res = 1
            return res
        flv_sign = False
        mp4_sign = False
        flv_spicial = False
        try:
            if self.is_flv(filelist[0]) and (site in self.sites):
                #flv_sign = True
                flv_spicial = True
                print "flv_spicial"
            elif self.is_flv(filelist[0]):
                flv_sign = True
                print "flv"
            elif self.is_mp4(filelist[0]):
                mp4_sign = True
                print "mp4"

            if mp4_sign:
                concat_mp4s(tuple(filelist),target_file)
            elif flv_sign:
                concat_flvs(tuple(filelist),target_file)
            elif flv_spicial:
                res = self.concat_flv2(tuple(filelist),target_file)
        except Exception, err:
            logging.error("cat_info " + str(err))
            try:
                if os.path.exists(target_file):
                    os.remove(target_file)
                if 0 != self.concat_mp4s2(filelist, target_file):
                    logging.error("cat_file error ,file is:" + str(target_file))
            except Exception, err:
                logging.error("cat_file error: " + str(err))
                res = 1
        try:
            filelen = len(filelist)
            for i in range(filelen):
                if os.path.exists(filelist[i]):
                    os.remove(filelist[i])
        except Exception, err:
            logging.error("remove file err " + str(err))
        return res

    def is_flv(self,filepath):
        result = True
        try:
            if not filepath or not os.path.exists(filepath) or not os.path.isfile(filepath):
                raise Exception()
            
            f = open(filepath, 'rb')
            header = f.read(3)
            if 'FLV' != header:
                result = False
        except Exception, err:
            logging.error("is_mp4" + str(err))
            result = False
        finally:
            f.close()
        return result

    def is_mp4(self,filepath):
        result = True
        try:
            if not filepath or not os.path.exists(filepath) or not os.path.isfile(filepath):
                raise Exception()
            f = open(filepath, 'rb')
            header = f.read(8)
            if len(header) < 8:
                result = False
            if 'ftyp' != header[4:]:
                result = False  
        except Exception, err:
            logging.error("is_mp4" + str(err))
            result = False
        finally:
            f.close()
        return result

    def command_execute(self,command):
        try:
            result = 0
            os_name = "Linux"
            if os_name == 'Linux':
                ret = os.system(command) >> 8
                if 0 != ret:
                    raise Exception()
            else:
                raise Exception()
        except Exception, err:
            result = -1
        finally:
            return result

    def concat_mp4s2(self,download_files_list, download_path):
        join_cmd = etc.mp4box_dir
        for tmp_download_file in download_files_list:
            join_cmd = join_cmd + ' -force-cat -cat ' + '"'+ str(tmp_download_file) + '"'
        join_cmd = join_cmd + ' -new ' + '"' + download_path + '"'
        print join_cmd
        #log.write('broker DownloadThread: concat_mp4s2 cmd = %s' % join_cmd)
        #log.flush()
        if 0 != self.command_execute(join_cmd):
            return -1
        else:
            return 0

    def concat_flv2(self,download_files_list,download_path):
        #./flv_project -operation combine -add ./v_19rrnwy16s_0 -add ./v_19rrnwy16s_1 -add ./v_19rrnwy16s_2 -add ./v_19rrnwy16s_3 -add ./v_19rrnwy16s_4 -add ./v_19rrnwy16s_5 -add ./v_19rrnwy16s_6 -add ./v_19rrnwy16s_7 -out ./v_19rrnwy16s
        join_cmd = etc.flv_project_dir
        tcmd = ""
        for tmp_download_file in download_files_list:
            tcmd = tcmd + " -add " + str(tmp_download_file)
        join_cmd = join_cmd + " -operation combine " + tcmd + " -out " + str(download_path)
        print join_cmd
        if 0 != self.command_execute(join_cmd):
            return "-1"
        else:
            return 0
        
