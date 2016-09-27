#!/usr/bin/python
# -*- coding:utf-8 -*- 
import logging
import logging.handlers
import json
import sys
#import tudou_cracker
import fivesix_cracker
import ku6_cracker
#import kkn_cracker
#import xl_cracker
#import cntv_cracker
#import sina_cracker
#import sohu_cracker
#import baomihua_cracker
#import ifeng_cracker

def parse_video_url(site,vid):
    parser_list = []
    #parser_list.append(("ifeng", ifeng_cracker.get_json_from_id, ifeng_cracker.get_video_url_and_type))
    #parser_list.append(("td",tudou_cracker.get_xml_from_id,tudou_cracker.get_video_url_and_type))
    parser_list.append(("56",fivesix_cracker.get_json_from_id,fivesix_cracker.get_video_url_and_type))
    parser_list.append(("k6",ku6_cracker.get_json_from_id,ku6_cracker.get_video_url_and_type))
    #parser_list.append(("kkn", kkn_cracker.get_m3u8_from_id, kkn_cracker.get_video_url_and_type))
    #parser_list.append(("cntv", cntv_cracker.get_json_from_id, cntv_cracker.get_video_url_and_type))
    #parser_list.append(("baomihua", baomihua_cracker.get_string_from_id, baomihua_cracker.get_video_url_and_type))
    #parser_list.append(("sina", sina_cracker.get_xml_from_id, sina_cracker.get_video_url_and_type))
    #parser_list.append(("xl", xl_cracker.get_json_from_id, xl_cracker.get_video_url_and_type))
    #parser_list.append(("sohu", sohu_cracker.get_htmlcontent_from_id, sohu_cracker.get_video_url_and_type))
    

    for parser in parser_list:
        if parser[0] == site:
            json_func =parser[1]
            parser_func = parser[2]
            jsoninfo = json_func(vid)
            if not jsoninfo:
                logging.error("pase info is None")
                return None
            url_list,filetype = parser_func(jsoninfo)
            if not url_list:
                logging.error("pase info,url is None")
                return None
            return url_list
    return [vid]


def get_video_url(info):
    try:
        logging.info("test : %s" % str(info))
        map_obj = json.loads(info)
        site = map_obj["site"]
        vid = map_obj["vid"]
        logging.info("site: %s" % str(site))
        logging.info("vid: %s" % str(vid))
        return parse_video_url(site,vid)
    except Exception,e:
        logging.error("get_video error: %s" % str(e))
        return None
