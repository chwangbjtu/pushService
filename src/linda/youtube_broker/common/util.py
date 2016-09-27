# -*- coding:utf-8 -*-
import os
import logging
import traceback
import etc

class Util(object):

    def search_file(self,filename,search_path):
        file_list = []
        try:
            #search_path = etc.download_path
            for pahth,subdirs,files in os.walk(search_path):
                for name in files:
                    if name.find(filename) >= 0:
                        file_list.append(name)
        except Exception, e:
            logging.error(traceback.format_exc()) 

        return file_list

    def get_file_ext(self,filename):
        file_ext = None
        try:
            info = filename.split(".")
            if len(info) >= 2:
                index = len(info)-1
                file_ext = info[index]
        except Exception, e:
            logging.error(traceback.format_exc())

        return file_ext

    def get_file_size(self,filename):
        file_size = None
        try:
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
        except Exception, e:
            logging.error(traceback.format_exc())

        return file_size

    #datapath,etc.download_path:path:get_task : dst_path (eg:media/linda/20150909/m23821/m1000)
    def create_data_dir(self,datapath,path):
        dirlist = path.split("/")
        tpath = datapath + dirlist[0] + "/" + dirlist[1] + "/" +  dirlist[2] + "/" + dirlist[3]
        res = False
        try:
            if not os.path.exists(tpath):
                os.makedirs(tpath)
            if os.path.exists(tpath):
                res = True
        except Exception, e:
            logging.error(traceback.format_exc())

        return res

    def get_download_file_path(slef,datapath,dst_path):
        filepath = ""
        try:
            dirlist = dst_path.split("/")
            filepath = datapath + dirlist[0] + "/" + dirlist[1] + "/" +  dirlist[2] + "/" + dirlist[3] + "/" 
        except Exception, e:
            logging.error(traceback.format_exc())

        return filepath

    #etc.download_path(eg:/tmp/)
    def del_data_dir(self,path):
        try:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
        except Exception, e:
            logging.error(traceback.format_exc())




if __name__ == '__main__':  
    #print filetype("/home/shiwg/loki/xvsync/xvsync/common/util.py") 
    util = Util()
    #print util.search_file("asdf")
    print util.get_file_ext("asdfa.sdf.mp4")
    print util.get_file_ext("asdf.asdf.flv")
