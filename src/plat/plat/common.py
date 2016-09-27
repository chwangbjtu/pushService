# -*- coding:utf-8 -*-

import logging
from difflib import SequenceMatcher
import math

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
        test_all()
    except Exception,e:
        logging.error(traceback.format_exc())
