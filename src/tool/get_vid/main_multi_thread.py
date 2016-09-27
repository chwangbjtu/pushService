# -*- coding:utf-8 -*-
import logging
import traceback
import json
import time
import threading
from util.util import logger_init
from database.db_connect import MysqlConnect
from database.ugc_dat_dao import UgcdatDao
from database.ugc_video_dao import UgcvideoDao
from http.http_client import HttpClient
from tornado import log

# global variable
thread_count = 10;
thread_index = range(thread_count);
threads_parser = [];
thread_update = None;

dat_ids = None;
db_conn = None;

def update_video_table():
    try:
       db_conn = MysqlConnect(name="ugc_test");
       if db_conn:
            ugcdat_dao = UgcdatDao(db_conn);

            dat_ids = ugcdat_dao.get_dat_ids();
            
            task_assign();
            
            db_conn.close();
    except Exception, e:
        db_conn.close();
        logging.error(traceback.format_exc());

def task_assign():
    try:
        dat_ids_count = len(dat_ids);
        step = dat_ids_count // thread_count;
        for index in thread_index:
            start = index * step;
            if index+1 == thread_count:
                end = dat_ids_count;
            else:
                end = start + step;
            t = threading.Thread(target=request_task_run, args=(start, end));
            t.setName(index);
            threads_parser.append(t);
        thread_update = threading.Thread(target=update_task_run, args=());
        for index in thread_index:
            threads_parser[index].start();
        
    except Exception, e:
        logging.error(traceback.format_exc());

def request_task_run(start, end)
    try:
        http_client = HttpClient();
        
        domain = "http://macross.funshion.com:27777";
        path = "/api/?cli=%s&cmd=%s&hashid=%%s" % ("video", "get_video_info_by_hashid",);
        url = domain + path;
        
        for item in dat_ids[start:end]
            dat_id = item["dat_id"];
            results = request_data(http_client, url, dat_id);

    except Exception, e:
        logging.error(traceback.format_exc());

def send_http_request(http_client, url, para):
    try:
        api = url % para;
        response_data = http_client.get_data(api);
        if response_data:
            result = parser_data(response_data[1]);
            return result;
        else:
            return [];
    except Exception, e:
        logging.error(traceback.format_exc());

def parser_data(data):
    try:
        json_data = json.loads(data);
        if json_data and json_data.keys():
            for key in json_data.keys():
                result = [];
                value = None;
                values = json_data[key];
                for item in values:
                    index = item.find("_");
                    if index != -1:
                        value = item[0:index];
                        break;
                result.append([key, value]);
            return result;
        else:
            print "json_data is None";
            return [];
    except Exception, e:
        logging.error(traceback.format_exc());

def update_task_run():
    try:
        
    except Exception, e:
        logggin.error(traceback.format_exc());


if __name__ == "__main__":
    try:
        logger_init();
        # test
        now = time.localtime(time.time());
        starttime = time.strftime("%Y-%m-%d %H:%M:%S", now);
        print "start time: %s" % starttime; 
        update_video_table();
        now = time.localtime(time.time());
        starttime = time.strftime("%Y-%m-%d %H:%M:%S", now);
        print "end time: %s" % starttime; 
    except Exception, e:
        logging.error(traceback.format_exc());
