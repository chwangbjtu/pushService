import traceback
import os
import logging
import logging.handlers
import urllib2
from kencode import *

def download(site,task_id,url,filename):
    """download methord"""
    logging.debug("site:%s,task_id : %s,url :%s,filename : %s",site,task_id,url,filename)
    res = 1
    length = 0
    recv_info_size = 0
    if not url or not filename:
        return res
    try:
        req = None
        f = None
        try:
            req = urllib2.Request(url)
            r = urllib2.urlopen(req, None, timeout = 60)
            recv_info = r.info()
            if 'Content-Type' not in recv_info:
                logging.error('broker Downloadthread: content_type error, task_id = %d, recv_info = \n%s' % (task_id, str(recv_info)))
                raise Exception()
            if 'Content-Length' not in recv_info:
                logging.error('broker Downloadthread: Content_Length error, task_id = %d, recv_info = \n%s' % (task_id, str(recv_info)))
                raise Exception()

            recv_info_size = int(recv_info['Content-Length'])
            #logging.debug("filename is %s" % filename)
            f = open(filename, 'wb')
        except Exception, err:
            logging.error("download error " + site + " task_id " + task_id + " url " + url + str(err))
            raise Exception()
        
        try:
            while True:
                recv_buffer = r.read(1024*256)
                if 0 == len(recv_buffer):
                    break
                f.write(recv_buffer)
        except Exception, err:
            logging.error("download error " + site + " task_id " + task_id + " url " + url + str(err))
            raise Exception()
        finally:
            f.close()
        real_write_size = os.path.getsize(utf8_to_local(filename))
        if real_write_size != recv_info_size:
            logging.error("download error "+site+" task_id "+task_id+" url "+url+" real write size:" + str(real_write_size) + " recv_size:" + str(recv_info_size))
            raise Exception()
        else:
            res = 0
            logging.info("download success "+site+" task_id "+task_id+" url "+url+" real write size:" + str(real_write_size) + " recv_size:" + str(recv_info_size))
    except Exception, err:
        logging.error("download error " + site + " task_id " + task_id + " url " + url + str(err))
        res = -1
    finally:
        return res
