# -*-coding:utf-8 -*-
import re
import time
import json
import hashlib
import traceback
from tornado import log

import sys
sys.path.append('.')
from conf import Conf
from common.util import create_id, timestamp2datetime, check_mysql
from common.util import PushMethod, PushType
from common.http_client import HttpClient
from common.mana_manager import ManaManager

class SyncManagement(object):
    
    def __init__(self):
        self.__http_client = HttpClient()
        self.__mana_manager = ManaManager()
        
        self._md5 = hashlib.md5()
        self._progress_interval_time = Conf.progress_interval_time
        self._progress_expire_time = Conf.progress_expire_time
        self._push_end_time = Conf.progress_expire_time * 2

        self._available_mtype = {"mplay":"media" , "vplay":"video"}
        self._android_mtype = {"mplay":"long", "vplay":"short"}
        self._ios_mtype = {"mplay":"mid1", "vplay":"mpurl"}
        #对于episode_type和chase_type这两个字段，通过走接口http://192.168.111.57:9876/api/?cmd=get_media_list
        #但该接口自2014-7-18起，都没有数据，所以字段采用默认的other类型

    def push(self, body_data):
        result = False
        try:
            data = body_data
            type = data['msg_type']
            if type != PushType.All:
                #待定，对于非全局推送，无需同步老版本
                log.app_log.info('sync management: failed, not global push')
                result = True
                return
            msgs = []
            msg_detail = json.loads(data['payload']['detail'])
            msg_data = [msg_detail]
            for msg in msg_data:
                msg_item = {}
                if 'mtype' not in msg or msg['mtype'] not in self._available_mtype:
                    continue
                msg_item['media_type'] = self._available_mtype[msg['mtype']]
                msg_item['android_msg_type'] = self._android_mtype[msg['mtype']]
                msg_item['ios_msg_type'] = self._ios_mtype[msg['mtype']]
                if 'msgid' not in msg or not msg['msgid']:
                    continue
                msg_item['msg_id'] = msg['msgid']
                if 'id' not in msg or not msg['id']:
                    continue
                msg_item['media_id'] = msg['id']
                url_result = {}
                if msg_item['media_type'] == 'media':
                    url_result = self.create_media_url(msg_item['media_id'])
                elif msg_item['media_type'] == 'video':
                    url_result = self.create_video_url(msg_item['media_id'])
                if not url_result:
                    continue
                msg_item['android_url'] = url_result['android']
                msg_item['ios_url'] = url_result['ios']
                if 'title' in msg:
                    msg_item['title'] = msg['title']
                if 'content' in msg:
                    msg_item['content'] = msg['content']
                    msg_item['android_content'] = msg['content']
                if 'poster' in msg:
                    msg_item['picture'] = msg['poster']
                if 'badge' in msg:
                    msg_item['badge'] = '0' 
                if 'style' in msg:
                    #msg_item['sf'] = msg['style']
                    msg_item['android_sf'] = msg['style'] 
                if 'still' in msg:
                    msg_item['logo'] = msg['still']
                if 'num' in msg:
                    msg_item['num'] = msg['num']
                msg_item['android_jump_flag'] = 1
                msg_item['user_name'] = 'admin'
                msg_item['check_state'] = 'success'
                msg_item['valid'] = 1
                msg_item['is_submmit'] = 1
                msgs.append(msg_item)
            if not msgs:
                log.app_log.info('sync management: failed, not valid msg')
                result = False
                return
            #首先插入到fs_msg_pool中，然后将msg插入到fs_msg_info中
            apps_dict = {}
            apps = self.__mana_manager.query_fs_app_info()
            for app in apps:
                app_id = app['app_id']
                #app_type是之前用于content_cache的
                apps_dict[app_id] = app['app_type']
            for msg in msgs:
                #跟management进行同步
                right = True
                msgid_bak = msg['msg_id']
                expire_time = int(time.time()) + self._progress_expire_time
                while int(time.time()) < expire_time: 
                    try:
                        push_ids = []
                        retry_times = 0
                        right = True
                        #插入fs_msg_pool
                        if 'msg_id' in msg:
                            msg.pop('msg_id')
                        if 'source_id' in msg:
                            msg.pop('source_id')
                        msg['is_submmit'] = 1
                        msg['check_state'] = 'success'
                        source_id = self.__mana_manager.insert_fs_msg_pool(msg, commit=False)
                        if not source_id:
                            log.app_log.info('sync management: sync msg_id(%s) insert fs_msg_pool failed: no source_id' % (msgid_bak,))
                            right = False
                            continue
                        #插入fs_msg_info
                        if 'is_submmit' in msg:
                            msg.pop('is_submmit')
                        if 'check_state' in msg:
                            msg.pop('check_state')
                        msg['msg_id'] = msgid_bak
                        msg['source_id'] = source_id
                        #给字段增加默认值，不能为null
                        msg['sound'] = ""
                        msg['description'] = ""
                        msg['media_tag'] = '[]'
                        msg['img'] = ""
                        msg['center_url'] = msg['logo']
                        msg_id = self.__mana_manager.update_insert_fs_msg_info(msg, commit=False)
                        if not msg_id:
                            log.app_log.info('sync management: source_id(%s) insert fs_msg_info failed: no msg_id' % (source_id,))
                            #删除掉fs_msg_pool中的source_id
                            self.__mana_manager.delete_fs_msg_pool(source_id)
                            right = False
                            continue
                        if not apps_dict:
                            apps_dict = {}
                            apps = self.__mana_manager.query_fs_app_info()
                            for app in apps:
                                app_id = app['app_id']
                                #app_type是之前用于content_cache的
                                apps_dict[app_id] = app['app_type']
                        for app_id in apps_dict: 
                            msg_push = {}
                            msg_push['msg_id'] = msgid_bak 
                            msg_push['app_id'] = app_id
                            msg_push['req'] = 0
                            msg_push['tt'] = 120
                            msg_push['rt'] = 0
                            msg_push['push_state'] = 'back-push'
                            msg_push['check_state'] = 'to-check'
                            #需要转换为日期格式
                            current_time = time.time()
                            current_time = timestamp2datetime(current_time)
                            if current_time:
                                msg_push['modify_time'] = current_time 
                            start_time = float(data['start_time'])
                            start_time = timestamp2datetime(start_time)
                            if start_time:
                                msg_push['push_begin_time'] = start_time 
                                msg_push['show_time'] = start_time
                            end_time = float(data['start_time']) + self._push_end_time
                            end_time = timestamp2datetime(end_time)
                            if end_time:
                                msg_push['push_end_time'] = end_time 
                            msg_push['is_valid'] = 1
                            #cmd_id对应着fs_cmd_info的cmd_id
                            msg_push['cmd_id'] = 2 
                            #if 'sf' in msg:
                            #    msg_push['sf'] = msg['sf'] 
                            #插入fs_msg_push
                            push_id = self.__mana_manager.update_insert_fs_msg_push(msg_push, commit=False)
                            if not push_id:
                                log.app_log.info('sync management: msg_id(%s) insert fs_msg_push failed: no push_id' % (msgid_bak,))
                                #删除掉fs_msg_pool中的source_id
                                self.__mana_manager.delete_fs_msg_pool(source_id)
                                #删除掉fs_msg_info中的msg_id
                                self.__mana_manager.delete_fs_msg_info(msgid_bak)
                                #删除掉fs_msg_push中的push_id
                                for push_id in push_ids:
                                    self.__mana_manager.delete_fs_msg_push(push_id)
                                push_ids = []
                                right = False
                                break
                            else:
                                push_ids.append(push_id)
                        if not push_ids:
                            #删除掉fs_msg_pool中的source_id
                            self.__mana_manager.delete_fs_msg_pool(source_id)
                            #删除掉fs_msg_info中的msg_id
                            self.__mana_manager.delete_fs_msg_info(msgid_bak)
                            right = False
                        #单个消息
                        if right:
                            break
                        retry_times = retry_times + 1
                        log.app_log.info('sync management: msg_id(%s) sync to management database: retry times(%s次)' % (msgid_bak, retry_times))
                        time.sleep(self._progress_interval_time)
                    except Exception, e:
                        right = False
                        result = False
                        if source_id:
                            self.__mana_manager.delete_fs_msg_pool(source_id)
                        if msgid_bak:
                            self.__mana_manager.delete_fs_msg_info(msgid_bak)
                        if push_ids:
                            for push_id in push_ids:
                                self.__mana_manager.delete_fs_msg_push(push_id)
                            push_ids = []
                        log.app_log.error(traceback.format_exc()) 
                        retry_times = retry_times + 1
                        time.sleep(self._progress_interval_time)
                #所有消息
                if not right:
                    result = False
                    return
            result = True
        except Exception, e:
            result = False
            log.app_log.error(traceback.format_exc()) 
        finally:
            return result

    def cancel(self, msgid, app_names=None):
        result = True
        expire_time = int(time.time()) + self._progress_expire_time
        while int(time.time()) < expire_time: 
            try:
                if not check_mysql():
                    time.sleep(self._progress_interval_time)
                    continue
                dict_data = {"push_state":"dismissed"}
                if app_names:
                    for app_name in app_names:
                        app_info = self.__mana_manager.query_by_app_name_fs_app_info(app_name=app_name, commit=False)
                        if app_info:
                            #数据库中有对应的app_name
                            app_id = app_info['app_id']
                            self.__mana_manager.update_fs_msg_push_by_msgid_appid(msgid, app_id, dict_data, commit=False)
                else:
                    self.__mana_manager.update_fs_msg_push_by_msgid(msgid, dict_data, commit=False)
                return result
            except Exception, e:
                result = False
                log.app_log.error(traceback.format_exc()) 
                time.sleep(self._progress_interval_time)

    def create_media_url(self, media_id):
        res = {}
        try:
            res['android'] = 'http://jsonfe.funshion.com/media/?cli=aphone&ver=1.5.1.3&sid=0002&mid=%s' % (media_id,)
            res['ios'] = media_id
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res

    def create_video_url(self, video_id):
        res = {}
        try:
            api_result = self.get_api_funshion(video_id)
            api_result = json.loads(api_result)
            hashid = api_result['data']['hashid']
            filename = api_result['data']['filename']
            if not hashid or not filename:
                return
            res['android'] = 'http://jobsfe.funshion.com/play/v1/mp4/%s.mp4?file=%s&f=z&clifz=aphone' % (hashid, filename)
            res['ios'] = 'http://jobsfe.funshion.com/query/v1/mp4/%s.json?file=%s&f=z&clifz=iphone' % (hashid, filename)
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res

    def get_api_funshion(self, video_id):
        res = None
        try:
            #'http://api.funshion.com/ajax/get_media_data/video/4459995'
            api_funshion_url = 'http://api.funshion.com/ajax/get_media_data/video/%s' % (video_id,)
            expire_time = int(time.time()) + self._progress_expire_time
            while int(time.time()) < expire_time: 
                try:
                    response = self.__http_client.get_data(api_funshion_url)
                    response = response['data'] if 'data' in response else response
                    log.app_log.debug('sync management: access server(%s) response:%s' % (api_funshion_url, response)) 
                    if not response:
                        log.app_log.debug('sync management: access server(%s) failed: need retry' % (api_funshion_url, ))
                    else:
                        res = response
                        break
                    time.sleep(self._progress_interval_time)
                except Exception, e:
                    log.app_log.error(traceback.format_exc()) 
                    time.sleep(self._progress_interval_time)
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res

if __name__ == '__main__':
    test = SyncManagement()
    res = test.get_api_funshion('4459995')
    print res
    res = test.create_media_url('4459995')
    print res
    res = test.create_video_url('4459995')
    print res
