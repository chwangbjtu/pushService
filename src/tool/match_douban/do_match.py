# -*- coding:utf-8 -*-
from db_connect import MysqlConnect
import traceback
import logging
import json
import re
from util import Util, logger_init
from funshion_dao import FunshionDao
from fdr_dao import FDRDao
from title_index_dao import TitleIndexDao
from director_index_dao import DirectorIndexDao
from actor_index_dao import ActorIndexDao
from difflib import SequenceMatcher
import math

def do_match_title():
    try:
        db_conn = MysqlConnect(name="xv")
        if db_conn:
            funshion_dao = FunshionDao(db_conn)
            fdr_dao = FDRDao(db_conn)
            title_index_dao =  TitleIndexDao(db_conn)
            director_index_dao =  DirectorIndexDao(db_conn)
            actor_index_dao =  ActorIndexDao(db_conn)

            videos = funshion_dao.get_video()
            for v in videos:
                fun_id = v['media_id']
                title = v['name']
                director = v['director']
                actor = v['actor']
                logging.info(fun_id)

                md5 = Util.cal_md5(title.strip())
                dou_ids = title_index_dao.get_did_by_title(md5)
                for dou_id in dou_ids:
                    dou_title = title_index_dao.get_title_by_did(dou_id)
                    dou_director = director_index_dao.get_director_by_did(dou_id)
                    dou_actor = actor_index_dao.get_actor_by_did(dou_id)

                    #cal fit
                    fit = cal_fit(v, {'title': dou_title, 'director': dou_director, 'actor': dou_actor})

                    #store or update
                    if not fdr_dao.check_rel(fun_id, dou_id):
                        fdr_dao.store_rel(fun_id, dou_id, fit)
                    else:
                        fdr_dao.update_rel(fun_id, dou_id, fit)

                    db_conn.commit()

            db_conn.close()

    except Exception,e:
        logging.error(traceback.format_exc())

def cal_similarity(elem_a, elem_b):
    return SequenceMatcher(None, elem_a, elem_b).ratio()

def cal_degree(src_group, dst_group, whole=False, ignore=False):
    degree = 0

    if src_group and dst_group:
        if ignore:
            count = len(src_group)
        else:
            count = max(len(src_group), len(dst_group))
        for elem in src_group:
            elem = elem.strip()
            if elem in dst_group:
                degree += 1.0 / count
            elif not whole:
                similarity = 0
                for elem_dst in dst_group:
                    val = cal_similarity(elem, elem_dst)
                    if val > similarity:
                        similarity = val
                degree += similarity / count

    return degree

def cal_fit(fun_v, dou_v):
    (title_w, director_w, actor_w) = (50, 20, 30)
    (title_f, director_f, actor_f) = (0, 0, 0)

    #title
    title = fun_v['name']
    if title:
        title_f = title_w * cal_degree([title], dou_v['title'], ignore=True)

    #director
    director = fun_v['director']
    if director:
        director_parts = director.split(',')
        director_f = director_w * cal_degree(director_parts, dou_v['director'])
    
    #actor
    actor = fun_v['actor']
    if actor:
        actor_parts = actor.split(',')
        actor_f = actor_w * cal_degree(actor_parts, dou_v['actor'])
    
    return int(math.ceil(title_f + director_f + actor_f))

def test_all():
    fun_v1 = {'name': u'一天一只猫', 'director': u'王为一,史东山', 'actor': u'达斯汀·哈夫曼,Steve McQueen'}
    fun_v2 = {'name': u'一天一只猫', 'director': u'王为一,史东山', 'actor': u'达斯汀·霍夫曼,Steve McQueen'}
    dou_v = {'title': [u'一日一猫', u'中古'], 'director': [u'王为一', u'史东山', u'史泰龙'], 'actor': [u'达斯汀·霍夫曼']}
    logging.info('fit: %s' % cal_fit(fun_v1, dou_v))
    logging.info('fit: %s' % cal_fit(fun_v2, dou_v))

if __name__ == "__main__":
    try:
        logger_init()

        #test_all()
        do_match_title()
    except Exception,e:
        logging.error(traceback.format_exc())
