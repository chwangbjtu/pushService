# -*- coding:utf-8 -*-
import logging
import traceback
import json
import time
from util.util import logger_init
from database.db_connect import MysqlConnect
from database.ugc_dat_dao import UgcdatDao
from database.ugc_video_dao import UgcvideoDao
from http.http_client import HttpClient

def export_video_id():
    try:
       db_conn = MysqlConnect(name="ugc");
       if db_conn:
            ugcvideo_dao = UgcvideoDao(db_conn)
            ugcvideo_dao.export_video_id()
            db_conn.commit()
            db_conn.close()
    except Exception, e:
        db_conn.close()
        logging.error(traceback.format_exc())

'''
def send_video_id():
    try:
       db_conn = MysqlConnect(name="ugc");
       if db_conn:
            ugcvideo_dao = UgcvideoDao(db_conn)
            vids = ugcvideo_dao.get_unsend_vid()
            
            if vids:
                total = len(vids)
                index = 0
                seg_inc = 10000
                print 'send total: %s' % total

                while index < total:
                    body = {"8800": [], "8801": [], "8802": [], "8803": []}
                    seg_index = 0
                    while seg_index < seg_inc and index + seg_index < total:
                        r = vids[index + seg_index]
                        if str(r['uid']) == '9':
                            body['8800'].append(r['vid'])
                        elif r['origin'] == 'forwards':
                            body['8801'].append(r['vid'])
                        elif r['origin'] == 'upload' and str(r['uid']) != '9':
                            body['8802'].append(r['vid'])
                        elif r['origin'] == 'push':
                            body['8803'].append(r['vid'])
                        seg_index += 1
                    
                    http_client = HttpClient()
                    url = 'http://192.168.8.194:9999/source/video'
                    res = http_client.post_data(url, json.dumps(body))
                    print res
                    if res and res[0] == 200:
                        res_json = json.loads(res[1])
                        if 'retcode' in res_json and str(res_json['retcode']) == '200':
                            ugcvideo_dao.set_send([[v['vid']] for v in vids[index:index + seg_index]])
                            db_conn.commit()
                    
                    print '%s - %s' % (index, index + seg_index - 1)
                    index += seg_index

            db_conn.close()
            
    except Exception, e:
        db_conn.close();
        logging.error(traceback.format_exc());
'''

def send_video_id():
    try:
       db_conn = MysqlConnect(name="ugc");
       if db_conn:
            ugcvideo_dao = UgcvideoDao(db_conn)

            while True:
                vids = ugcvideo_dao.get_unsend_vid(count=1000)
                if vids:
                    body = {"8800": [], "8801": [], "8802": [], "8803": []}
                    for r in vids:
                        if str(r['uid']) == '9':
                            body['8800'].append(r['vid'])
                        elif r['origin'] == 'forwards':
                            body['8801'].append(r['vid'])
                        elif r['origin'] == 'upload' and str(r['uid']) != '9':
                            body['8802'].append(r['vid'])
                        elif r['origin'] == 'push':
                            body['8803'].append(r['vid'])
                    
                    http_client = HttpClient()
                    url = 'http://192.168.8.194:9999/source/video'
                    res = http_client.post_data(url, json.dumps(body))
                    #print res
                    if res and res[0] == 200:
                        res_json = json.loads(res[1])
                        if 'retcode' in res_json and str(res_json['retcode']) == '200':
                            ugcvideo_dao.set_send([[v['vid']] for v in vids])
                            db_conn.commit()
                    
                    print 'get: %s' % (len(vids),)
                else:
                    break

            db_conn.close()
            
    except Exception, e:
        db_conn.close();
        logging.error(traceback.format_exc());

def update_video_table():
    try:
       db_conn = MysqlConnect(name="ugc");
       if db_conn:
            ugcdat_dao = UgcdatDao(db_conn);
            ugcvideo_dao = UgcvideoDao(db_conn);

            http_client = HttpClient();
            domain = "http://macross.funshion.com:27777";
            path = "/api/?cli=%s&cmd=%s&hashid=%%s" % ("video", "get_video_info_by_hashid",);
            url = domain + path;

            #dat_ids = ugcdat_dao.get_dat_ids();
            dat_ids = ugcdat_dao.get_dat_ids_inc();
            for item in dat_ids:
                dat_id = item["dat_id"];
                result = send_http_request(http_client, url, (dat_id,));
                if result:
                    for item2 in result:
                        print '%s--%s' % (item2[0], item2[1])
                        ugcvideo_dao.update_video_id(item2[0], item2[1]);
                    db_conn.commit();
            db_conn.close();
    except Exception, e:
        db_conn.close();
        logging.error(traceback.format_exc());

def send_http_request(http_client, url, para):
    try:
        api = url % para;
        response_data = http_client.get_data(api);
        print response_data
        if response_data:
            result = parser_data(response_data[1]);
            return result;
        else:
            return [];
    except Exception, e:
        logging.error(traceback.format_exc());

def parser_data(data):
    try:
        dict_data = json.loads(data)
        result = []
        if dict_data:
            for k,v in dict_data.items():
                if v:
                    videos = v[0].split('_')
                    if videos:
                        video_id = videos[0]
                        result.append([k, video_id]);
            return result;

    except Exception, e:
        logging.error(traceback.format_exc());


if __name__ == "__main__":
    try:
        logger_init();

        #get new vid
        now = time.localtime(time.time());
        starttime = time.strftime("%Y-%m-%d %H:%M:%S", now);
        print "start time: %s" % starttime; 
        update_video_table();
        now = time.localtime(time.time());
        starttime = time.strftime("%Y-%m-%d %H:%M:%S", now);
        print "end time: %s" % starttime; 
        '''
        '''

        '''
        print "export video_ids"
        export_video_id()
        print "dones"
        '''
        
        #send vid
        print "send video_ids"
        send_video_id()
        print "dones"

    except Exception, e:
        logging.error(traceback.format_exc());
