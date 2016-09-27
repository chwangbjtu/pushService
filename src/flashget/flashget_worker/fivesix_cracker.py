import logging
import logging.handlers
import json
import urllib2_thread_wrapper
import url_helper

def get_json_from_id(id):
    json_url = "http://vxml.56.com/json/%s/?src=site" % id
    try:
        logging.info("")
        opener = urllib2_thread_wrapper.get_opener()
        logging.info("")
        response = opener.open(json_url, timeout = 30)
        logging.info("")
        content = response.read()
        logging.info("")
    except Exception,e:
        logging.error("get josn error: %s " % str(e))
        return None
    return content

def get_video_url_and_type(jsoninfo):
    urls = []
    try:
        result = json.loads(jsoninfo)
        rfiles = result["info"]["rfiles"]
        type_seq = ["wvga","super","vga","clear","qvga","normal","qqvga"]
        for file_type in type_seq:
            for item in rfiles:
                if item["type"] == file_type:
                    urls.append(item["url"])
                    break
            if urls:
                break
        if not urls:
            return (None,None)
        filetype = url_helper.get_file_type(urls[0])
        return (urls,filetype)
    except:
        return (None,None)


