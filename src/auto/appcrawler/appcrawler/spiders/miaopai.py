# -*- coding:utf-8 -*-
import time
import json
import traceback
import logging
from scrapy.spiders import Spider
from scrapy.http import Request
from appcrawler.items import EpisodeItem
from appcrawler.db.db_mgr import DbManager


class MiaoPai(Spider):
    '''
    '''
    name = 'miaopai'
    site_code = 'miaopai'
    dbmgr = DbManager.instance()
    max_page_num = 100

    def __init__(self, *args, **kwargs):
        super(MiaoPai, self).__init__(*args, **kwargs)
        self.site_id = self.dbmgr.get_site_id_by_code(self.site_code)
        self.api = "http://api.miaopai.com/m/cate2_channel?cateid=%s&page=%s"

    def start_requests(self):
        try:
            page_num = 1
            task = self.dbmgr.get_miaopai_task()
            for t in task:
                mpc_id, mpc_name = t
                r = Request(url=self.api % (mpc_id, page_num), callback=self.parse_media)
                r.meta.update({'mpc_id':mpc_id, 'page_num':page_num, 'mpc_name':mpc_name})
                yield r
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

    def parse_media(self, response):
        try:
            logging.log(logging.INFO, 'parse_media: %s' % response.request.url)
            mpc_id = response.request.meta['mpc_id']
            page_num = response.request.meta['page_num']
            channel_name = mpc_name = response.request.meta['mpc_name']

            jdata = json.loads(response.body)
            result = jdata.get('result', [])
            for r in result:
                try:
                    channel = r.get('channel')
                    if not channel:
                        continue

                    cont_id = scid = channel.get('scid')
                    if not cont_id:
                        continue

                    played = vcnt = channel.get('stat', {}).get('vcnt')

                    base = channel.get('pic', {}).get('base')
                    m = channel.get('pic', {}).get('m')
                    if base and m:
                        thumb_url = base + m
                    else:
                        thumb_url = ''

                    base = channel.get('stream', {}).get('base')
                    sign = channel.get('stream', {}).get('sign', '')
                    if base and sign:
                        if '.mp4' not in base:
                            url = base + cont_id +'.mp4?vend=miaopai&' + sign
                        else:
                            url = base + sign
                    else:
                        continue

                    title = ft = channel.get('ext', {}).get('ft')
                    if not title:
                        title = t = channel.get('ext', {}).get('t')
                    if not title:
                        continue

                    # seconds
                    duration = length = channel.get('ext', {}).get('length')

                    cp_name = nick = channel.get('ext', {}).get('owner', {}).get('nick', '')

                    topicinfo = channel.get('topicinfo', [])
                    topicinfo = '|'.join(topicinfo)
                    tag = mpc_name
                    if cp_name:
                        tag = tag + '|' + cp_name
                    if topicinfo:
                        tag = tag + '|' + topicinfo

                    createTime = channel.get('ext2', {}).get('createTime')
                    if createTime and type(createTime) == int:
                        utime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(createTime/1000.0))
                    else:
                        utime = None

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
                    ep_item['channel_name'] = channel_name


                    yield ep_item
                except Exception, e:
                    logging.log(logging.ERROR, traceback.format_exc())
                    continue

            if page_num < self.max_page_num:
                r = Request(url=self.api % (mpc_id, page_num+1), callback=self.parse_media)
                r.meta.update({'mpc_id':mpc_id, 'page_num':page_num+1, 'mpc_name':mpc_name})
                yield r
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())


