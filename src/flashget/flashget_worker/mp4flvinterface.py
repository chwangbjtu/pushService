#!/home/admin/broker_project/build_tools/python272/bin/python
# -*- coding:utf-8 -*- 

import traceback
import os
import urllib2
from flvjoin import *
from mp4join import *
from kencode import *
from res_type import *

READ_UNIT = 256 * 1024


if 'Windows'==platform.system():
    pass
else:
    if 'LD_LIBRARY_PATH' in os.environ:
        if os.environ['LD_LIBRARY_PATH'].find('./tools/ffmpeg/lib/:./tools/lib/') < 0:
            value = './tools/ffmpeg/lib/:./tools/lib/' + ':' + os.environ['LD_LIBRARY_PATH'] 
            os.environ['LD_LIBRARY_PATH'] = value
    else:
        os.environ['LD_LIBRARY_PATH'] = './tools/ffmpeg/lib/:./tools/lib/'
    print os.environ['LD_LIBRARY_PATH']
    log.write('broker Downloadthread: load lib path = %s' % os.environ['LD_LIBRARY_PATH'])
    log.flush()

def command_execute(command):
    try:
        result = 0
        os_name = platform.system()
        if os_name == 'Windows':
            ret = os.system(command)
            if 0 != ret:
                raise Exception()
        elif os_name == 'Linux':
            ret = os.system(command) >> 8
            if 0 != ret:
                raise Exception()
        else:
            print 'platform not supported'
            raise Exception()
    except:
        result = -1
    finally:
        return result

def download_old(url, filepath):
    """download methord"""
    if not url or not filepath:
        return RES_PARAMS_ERROR
    try:
        req = urllib2.Request(url)
        r = urllib2.urlopen(req)
        f = open(filepath, 'wb')
        f.write(r.read())
        f.close()
    except:
        return RES_FAIL
    finally:
        return RES_SUCCESS

def download(url, filepath, task_id):
    """download methord"""
    res = 0
    length = 0
    recv_info_size = 0
    if not url or not filepath:
        return res
    try:
        req = None
        f = None
        f = None
        try:
            req = urllib2.Request(url)
            r = urllib2.urlopen(req, None, timeout = 60)
            recv_info = r.info()
            print 'recv info task_id = %d, recv_info = \n%s' % (task_id, str(recv_info))
            log.write('broker Downloadthread: recv info task_id = %d, recv_info = \n%s' % (task_id, str(recv_info)))
            log.flush()
            if 'Content-Type' not in recv_info:
                log.write('broker Downloadthread: content_type error, task_id = %d, recv_info = \n%s' % (task_id, str(recv_info)))
                log.flush()
                raise Exception()
            if 'Content-Length' not in recv_info:
                log.write('broker Downloadthread: content_length error, task_id = %d, recv_info = \n%s' % (task_id, str(recv_info)))
                log.flush()
                raise Exception()
            if 'text/html' == recv_info['Content-Type']:
                log.write('broker Downloadthread: texthtml content_type error, task_id = %d, recv_info = \n%s' % (task_id, str(recv_info)))
                log.flush()
                raise Exception()
            recv_info_size = int(recv_info['Content-Length'])
            f = open(filepath, 'wb')
        except:
            print 'urllib2 connect error or open file for reading error'
            exception = traceback.format_exc()
            log.write('broker Downloadthread: downlaoding time out error, task_id = %d, url = %s, filepath = %s, exception = %s' % (task_id, url, filepath, exception))
            log.flush()
            raise Exception()
        

        try:

            while True:
                recv_buffer = r.read(1024*256)
                if 0 == len(recv_buffer):
                    break
                f.write(recv_buffer)
                # length = length + len(recv_buffer)


            # need_read_size = recv_info_size
            # while need_read_size > 0:
            #     if need_read_size > READ_UNIT:
            #         read_size =  READ_UNIT
            #     else:
            #         read_size = need_read_size
            #     recv_buffer = r.read(read_size)
            #     f.write(recv_buffer)
            #     need_read_size = need_read_size - len(recv_buffer)
                # print need_read_size

        except:
            print 'reading or writing error'
            exception = traceback.format_exc()
            print exception
            log.write('broker Downloadthread: downlaoding reading or writing error, task_id = %d, url = %s, filepath = %s, exception = %s' % (task_id, url, filepath, exception))
            log.flush()
            raise Exception()
        finally:
            f.close()

        real_write_size = os.path.getsize(utf8_to_local(filepath))
        if real_write_size != recv_info_size:
            print 'broker Downloadthread: download function error, task_id = %d, real write size: %d\nrecv_info_size: %d' % (task_id, real_write_size, recv_info_size)
            log.write('broker Downloadthread: download function error, task_id = %d, real write size = %d, recv_info_size = %d' % (task_id, real_write_size, recv_info_size))
            log.flush()
            raise Exception()
        else:
            log.write('broker Downloadthread: download success, task_id = %d, real write size = %d, recv_info_size = %d' % (task_id, real_write_size, recv_info_size))
            log.flush()
    except:
        exception =  traceback.format_exc()
        print exception
        log.write('broker Downloadthread: downlaoding error, traceback in [task_id = %d, download(url, filepath)] exception = %s' % (task_id, exception))
        log.flush()
        res = -1
    finally:
        return res

def is_flv_file(file_path):
    result = True
    try:
        if not file_path:
            print 'no path'
            raise Exception()
        if not os.path.exists(utf8_to_local(file_path)):
            print 'file does not exist'
            raise Exception()
        if not os.path.isfile(utf8_to_local(file_path)):
            print 'path you input is not a file'
            raise Exception()
        try:
            f = open(utf8_to_local(file_path), 'rb')
        except:
            print 'open file for reading error'
            raise Exception()
        try:
            header = f.read(3)
        except:
            print 'read header error'
            raise Exception()
        else:
            if 'FLV' != header:
                result = False
        finally:
            f.close()
    except:
        exception =  traceback.format_exc()
        log.write('broker Downloadthread: is_flv_file error, %s' % exception)
        log.flush()
        result = False
    finally:
        return result

def is_mp4_file(file_path):
    result = True
    try:
        if not file_path:
            print 'no path'
            raise Exception()
        if not os.path.exists(utf8_to_local(file_path)):
            print 'file does not exist'
            raise Exception()
        if not os.path.isfile(utf8_to_local(file_path)):
            print 'path you input is not a file'
            raise Exception()
        try:
            f = open(utf8_to_local(file_path), 'rb')
        except:
            print 'open file for reading error'
            raise Exception()
        try:
            header = f.read(8)
        except:
            print 'read header error'
            raise Exception()
        else:
            if len(header) < 8:
                result = False
            if 'ftyp' != header[4:]:
                result = False  
        finally:
            f.close()
    except:
        exception =  traceback.format_exc()
        log.write('broker Downloadthread: is_mp4_file error, %s' % exception)
        log.flush()
        result = False
    finally:
        return result

'''including single file'''
def dowload_files(url_list, down_load_path, task_id, retry_times):
    result = 0
    try:
        tmp_download_file_path = UGC_PATH + os.path.sep + str(task_id) + os.path.sep + 'tmpdown'
        url_list_len = len(url_list)
        log.write('broker DownloadThread : url_list_len = %d, task_id = %d' % (url_list_len, task_id))
        log.flush()
        if 0 == url_list_len:
            log.write('broker DownloadThread : url_list_len = %d, task_id = %d error' % (url_list_len, task_id))
            log.flush()
            raise Exception()
        elif 1 == url_list_len:
            res = download_single_file(url_list[0], down_load_path, retry_times, task_id)
            if 0 != res:
                log.write('broker DownloadThread : download single file error, task_id = %d, path = %s' % (task_id, down_load_path))
                log.flush()
                raise Exception()
            else:
                log.write('broker DownloadThread : download single file success, task_id = %d, path = %s' % (task_id, down_load_path))
                log.flush()
        else:
            # if not os.path.exists(utf8_to_local(TMP_DOWNLOAD_FILE_PATH)):
            #     os.makedirs(utf8_to_local(TMP_DOWNLOAD_FILE_PATH))
            log.write('broker DownloadThread : download multiple files, task_id = %d' % task_id)
            log.flush()
            if not os.path.exists(utf8_to_local(tmp_download_file_path)):
                os.makedirs(utf8_to_local(tmp_download_file_path))
            i = 0
            flv_sign = False
            mp4_sign = False
            tmp_download_file_list = []
            for url in url_list:
                tmp_download_file = tmp_download_file_path + os.path.sep + str(i)
                if 0 != download_single_file(url, tmp_download_file, retry_times, task_id):
                    log.write('broker DownloadThread : download file error in multiple files [file = %s, task_id = %d, url = %s]' % (tmp_download_file, task_id, url))
                    log.flush()
                    raise Exception()
                else:
                    log.write('broker DownloadThread : download file success in multiple files [file = %s, task_id = %d, url = %s]' % (tmp_download_file, task_id, url))
                    log.flush()

                if is_flv_file(tmp_download_file):
                    flv_sign = True
                elif is_mp4_file(tmp_download_file):
                    mp4_sign = True
                else:
                    log.write('broker DownloadThread : formats error. task_id = %d' % task_id)
                    log.flush()
                    raise Exception()
                if flv_sign and mp4_sign:
                    log.write('broker DownloadThread : mp4 flv error. task_id = %d' % task_id)
                    log.flush()
                    raise Exception()
                tmp_download_file_list.append(tmp_download_file)
                i += 1
            log.write('broker DownloadThread : before concat task_id = %d' % task_id)
            log.flush()
            if flv_sign:
                concat_flvs(tuple(tmp_download_file_list), down_load_path)
            if mp4_sign:
                try:
                    concat_mp4s(tuple(tmp_download_file_list), down_load_path)
                except:
                    exception = traceback.format_exc()
                    print exception
                    log.write('broker DownloadThread :  concat_mp4s error, task_id = %d, exception = %s, fils = %s' % (task_id, exception, str(tmp_download_file_list)))
                    log.flush()

                    if os.path.exists(utf8_to_local(down_load_path)):
                        os.remove(utf8_to_local(down_load_path))

                    if 0 != concat_mp4s2(tmp_download_file_list, down_load_path):
                        log.write('broker DownloadThread :  mp4box concat_mp4s2 error, task_id = %d, exception = %s, files = %s' % (task_id, exception, str(tmp_download_file_list)))
                        log.flush()
                        raise Exception()

            log.write('broker DownloadThread : after concat task_id = %d' % task_id)
            log.flush()
    except:
        result = -1
        exception =  traceback.format_exc()
        log.write('broker DownloadThread : %s dowload_files failure, task_id = %d' % (exception, task_id))
        log.flush()
    finally:
        return result

def concat_mp4s2(download_files_list, download_path):
    join_cmd = mp4box_dir
    for tmp_download_file in download_files_list:
        join_cmd = join_cmd + ' -force-cat -cat ' + '"'+ str(tmp_download_file) + '"'
    join_cmd = join_cmd + ' -new ' + '"' + download_path + '"'
    print join_cmd
    log.write('broker DownloadThread: concat_mp4s2 cmd = %s' % join_cmd)
    log.flush()
    if 0 != command_execute(join_cmd):
        return -1
    else:
        return 0


def download_single_file(url, download_path, retry_times, task_id):
    log.write('broker DownloadThread :url = %s, download_path =%s, retry_times = %d, task_id = %d' % (url, download_path, retry_times, task_id))
    log.flush()
    res = -1
    for i in range(retry_times):
        log.write('broker DownloadThread :url = %s, download_path =%s, times = %d, task_id = %d' % (url, download_path, i, task_id))
        log.flush()
        res = download(url, download_path, task_id)
        if 0 == res:
            break
    return res

if __name__ == '__main__':
    # print is_mp4_file('d:\\1.mp4')
    # print is_flv_file('d:\\xun.flv')
    # req = urllib2.Request('http://domhttp.kksmg.com/2013/09/18/h264_450k_mp4_SHDongFangHD2500000201309183861811054_aac.mp4')
    # r = urllib2.urlopen(req, None, 10)
    #print download('http://domhttp.kksmg.com/2013/09/18/h264_450k_mp4_SHDongFangHD2500000201309183861811054_aac.mp4', 'd:\\xxx.mp4', 77)
    # print r.geturl()
    # print r.info()
    pass