# -*- coding:utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from appcrawler.db.db_mgr import DbManager
from appcrawler.items import EpisodeItem
import logging
import traceback


class MysqlStorePipeline(object):
    def __init__(self):
        self.__db_mgr = DbManager.instance()

    def process_item(self, item, spider):
        try:
            if isinstance(item, EpisodeItem):
                self.__db_mgr.insert_episode(item)
            return item
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

