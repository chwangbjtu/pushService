import os
import logging
import logging.handlers
from mp4join import *
from flvjoin import *

class joinfile:
    def concat_file(self,task_id,filelist,down_load_path):
        flv_sign = False
        mp4_sign = False
        tmp_download_file_list = []
        logging.debug("test1")
        logging.debug("filelist len %d",len(filelist))
        for tmp_download_file in filelist:
            if self.is_flv_file(tmp_download_file):
                flv_sign = True
            elif self.is_mp4_file(tmp_download_file):
                mp4_sign = True
            else:
                logging.info('broker DownloadThread : formats error. task_id = %d' % task_id)
                raise Exception()
            if flv_sign and mp4_sign:
                logging.info('broker DownloadThread : mp4 flv error. task_id = %d' % task_id)
                raise Exception()
            tmp_download_file_list.append(tmp_download_file)
            #i += 1
        logging.debug("test2")
        #logging.info('broker DownloadThread : before concat task_id = %d' % task_id)
        if flv_sign:
            logging.debug("test3")
            concat_flvs(tuple(tmp_download_file_list), down_load_path)
            logging.debug("test4")
        if mp4_sign:
            logging.debug("test4.5")
            try:
                logging.debug("test5")
                concat_mp4s(tuple(tmp_download_file_list), down_load_path)
            except:
                exception = traceback.format_exc()
                print exception
                logging.debug("test6")
                logging.info('broker DownloadThread :  concat_mp4s error, task_id = %d, exception = %s, fils = %s' % (task_id, exception, str(tmp_download_file_list)
))
                logging.debug("test7")

                if os.path.exists(utf8_to_local(down_load_path)):
                    logging.debug("test8")
                    os.remove(utf8_to_local(down_load_path))
                if 0 != self.concat_mp4s2(tmp_download_file_list, down_load_path):
                    logging.debug("test59")
                    logging.info('broker DownloadThread :  mp4box concat_mp4s2 error, task_id = %d, exception = %s, files = %s' % (task_id, exception, str(tmp_download_file_list)))
                    raise Exception()

    def concat_mp4s2(self,download_files_list, download_path):
        join_cmd = mp4box_dir
        for tmp_download_file in download_files_list:
            join_cmd = join_cmd + ' -force-cat -cat ' + '"'+ str(tmp_download_file) + '"'
        join_cmd = join_cmd + ' -new ' + '"' + download_path + '"'
        print join_cmd
        logging.info('broker DownloadThread: concat_mp4s2 cmd = %s' % join_cmd)
        if 0 != command_execute(join_cmd):
            return -1
        else:
            return 0


    def is_flv_file(self,file_path):
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
            logging.error('broker Downloadthread: is_flv_file error, %s' % exception)
            result = False
        finally:
            return result

    def is_mp4_file(self,file_path):
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
            logging.error('broker Downloadthread: is_mp4_file error, %s' % exception)
            result = False
        finally:
            return result




