# -*- coding:utf-8 -*-
import time
import json
import traceback
import logging
from scrapy.spiders import Spider
from scrapy.http import Request
from appcrawler.items import EpisodeItem
from appcrawler.db.db_mgr import DbManager


class TouTiao(Spider):
    '''
    '''
    name = 'toutiao'
    site_code = 'toutiao'
    dbmgr = DbManager.instance()
    max_page_num = 500

    def __init__(self, *args, **kwargs):
        super(TouTiao, self).__init__(*args, **kwargs)
        self.site_id = self.dbmgr.get_site_id_by_code(self.site_code)
        #self.api = "http://api.miaopai.com/m/cate2_channel?cateid=%s&page=%s"
        self.url_first = "http://toutiao.com/api/article/recent/?source=2&category=video&as=A165771AD802ED5&cp=57A8D2FE6D658E1&_=%s"
        self.url_second = "http://toutiao.com/api/article/recent/?source=2&count=20&category=video&max_behot_time=%s&utm_source=toutiao&offset=0&as=A1A5A75A8882EDC&cp=57A852EE9D5C6E1&_=%s"
    def start_requests(self):
        try:
            items = []
            url = self.url_first % int(time.time())
            items.append(Request(url=url, callback=self.parse_media,meta={"page_num":0}))
            return items
            '''
            page_num = 1
            task = self.dbmgr.get_miaopai_task()
            for t in task:
                mpc_id, channel_id, mpc_name = t
                r = Request(url=self.api % (mpc_id, page_num), callback=self.parse_media)
                r.meta.update({'mpc_id':mpc_id, 'channel_id':channel_id, 'page_num':page_num, 'mpc_name':mpc_name})
                yield r
            '''
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

    def parse_media(self, response):
        try:
            items = []
            logging.log(logging.INFO, 'parse_media: %s' % response.request.url)
            page_num = response.request.meta['page_num']
            if not page_num:
                page_num = 0
            jdata = json.loads(response.body)
            has_more = jdata.get("has_more")
            message = jdata.get("message")
            next_info = jdata.get("next")
            max_behot_time = next_info.get("max_behot_time")
            result = jdata.get('data', [])
            for r in result:
                try:
                    cont_id = r["id"]
                    title = r["title"]
                    url = r["url"]
                    thumb_url = r["image_url"]
                    if "video_duration" in r:
                        duration = r["video_duration"]
                    else:
                        duration = 0
                    cp_name = r["media_name"]
                    tag = r["keywords"]+","
                    tag = tag+cp_name
                    tag = tag.replace(',','|').strip('|')
                    played = r["video_play_count"]
                    utime = r["create_time"]
                    utime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utime))
                    ep_item = EpisodeItem()
                    ep_item['cont_id'] = cont_id
                    ep_item['site_id'] = self.site_id
                    ep_item['title'] = title
                    ep_item['url'] = url
                    if thumb_url:
                        ep_item['thumb_url'] = thumb_url
                    if duration:
                        ep_item['duration'] = duration
                    if cp_name:
                        ep_item['cp_name'] = cp_name
                    ep_item['tag'] = tag
                    if played:
                        ep_item['played'] = played
                    if utime:
                        ep_item['utime'] = utime
                    ep_item['channel_name'] = r["tag"]


                    items.append(ep_item)
                except Exception, e:
                    #logging.log(logging.ERROR, traceback.format_exc())
                    #logging.log(logging.ERROR, str(r))
                    continue
            #'''
            if page_num < self.max_page_num:
                second_url = self.url_second % (max_behot_time,int(time.time()))
                items.append(Request(url=second_url,callback=self.parse_media,meta={'page_num':page_num+1}))
                return items
            else:
                return items
            #'''
            return items
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())
            logging.log(logging.ERROR, str(jdata))
            return items

