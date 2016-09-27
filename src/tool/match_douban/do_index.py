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
from douban_dao import DoubanDao

cn_re = re.compile(ur'.*[\u4e00-\u9fa5]+')

def index_title(title):
    try:
        sp = re.match(cn_re, title)

        #not contain chinese
        if sp:
            parts = title.split()
            if len(parts) > 1:
                part1 = parts[0].strip()
                part2 = parts[1].strip()
                if re.match(ur'第.+季', part2):
                    part1 += part2
                return [part1]
        return [title.strip()]
    except Exception, e:
        logging.error(traceback.format_exc())

def index_aka(aka):
    try:
        parts = aka.split('/')
        res = []
        for p in parts:
            sp = re.match(cn_re, p)
            if sp:
                res.append(p.replace(' ', ''))
            else:
                res.append(p.strip())
        return res
    except Exception, e:
        logging.error(traceback.format_exc())

def do_index():
    try:
        db_conn = MysqlConnect(name="xv")
        if db_conn:
            title_index_dao =  TitleIndexDao(db_conn)
            director_index_dao =  DirectorIndexDao(db_conn)
            actor_index_dao =  ActorIndexDao(db_conn)
            douban_dao = DoubanDao(db_conn)

            videos = douban_dao.get_video()
            for v in videos:
                show_id = v['show_id']
                title = v['title']
                aka = v['aka']
                director = v['director']
                actor = v['actor']
                logging.info(show_id)

                ts = []
                if title:
                    ts.extend(index_title(title))
                if aka:
                    ts.extend(index_aka(aka))
                #store
                for t in ts:
                    #title
                    md5 = Util.cal_md5(t)
                    ct = title_index_dao.check_title(show_id, md5)

                    if ct:
                        if ct != t:
                            logging.info('show_id %s exit, but title not consistent: %s' % (show_id, ct))
                    else:
                        title_index_dao.store_title(t, show_id, md5)
                        db_conn.commit()

                    #director
                    ds = []
                    if director:
                        parts = director.split(',')
                        for p in parts:
                            ds.append(p.strip())
                    for d in ds:
                        cd = director_index_dao.check_director(show_id, d)
                        if not cd:
                            director_index_dao.store_director(show_id, d)
                            db_conn.commit()

                    #actor
                    cs = []
                    if actor:
                        parts = actor.split(',')
                        for p in parts:
                            cs.append(p.strip())
                    for c in cs:
                        cc = actor_index_dao.check_actor(show_id, c)
                        if not cc:
                            actor_index_dao.store_actor(show_id, c)
                            db_conn.commit()

            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())

def test_title():
    try:
        test = [u'恩赐之地 第一季 Graceland Season 1', u'本垒打 Home Run', u'Das Ekel', u'A计划', u'Hocuspocus', u'恋爱SOS', u'傻人大牛', u'纪戊~警视厅特殊犯搜查系 ジウ～警視庁特殊犯捜査係', u'家，N次方', u'许巍：此时此刻', u'台风 태풍', u'无耻之徒(美版) 第一季 Shameless Season 1', u'開門之前，意外之後 Avalon', u'愛！愛！愛！ Magi i luften', u'团结，团结…… Solidarność, Solidarność...']
        for t in test:
            logging.info('%s----%s' % (t, ",".join(index_title(t))))
    except Exception,e:
        logging.error(traceback.format_exc())

def test_aka():
    try:
        aka = [u'牛犊 / 金牛座 / 列宁最后的日子 / Taurus', u'Vremya tantsora / Time of a Dancer', u'囧男孩看世界(台) / 梅尼诺EO的世界 / The Boy and the World']
        for t in aka:
            logging.info('%s----%s' % (t, ",".join(index_aka(t))))
    except Exception,e:
        logging.error(traceback.format_exc())

def test_all():
    test_title()
    test_aka()

if __name__ == "__main__":
    try:
        logger_init()

        test_all()
        do_index()
    except Exception,e:
        logging.error(traceback.format_exc())
