# -*- coding:utf-8 -*-
from tornado import httpclient
from tornado import log
import json
 
class HttpClient(object):
    
    def __init__(self):
        self._http_client = httpclient.HTTPClient()

    def post_data(self, url, body):
        try:
            request = httpclient.HTTPRequest(url=url, method="POST", body=body)
            response = self._http_client.fetch(request)
            return (response.code, response.body)
        except httpclient.HTTPError,e:
            log.app_log.error("post error: [%s] [%s] [%s]" % (url, body, e))
            return ('', '')
 
if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from common.conf import Conf
    content = \
        {
            "user": "kuaikan",
            "content": [
                {
                    "vid": "XOTQ5NjMyMzgw",
                    "url": "http://v.youku.com/v_show/id_XOTQ5NjMyMzgw.html",
                    "title": "视频: 俄空军王牌战机 亮相莫斯科卫国战争胜利70周年阅兵彩排 2015 5.5",
                    "category": "快看",
                    "tag": "莫斯科|阅兵",
                    "pub_time": "2014-09-24 06:06:19",
                    "description": "俄空军王牌战机 亮相莫斯科卫国战争胜利70周年阅兵彩排 2015 5.5 俄罗斯记念1941-1945年卫国战争胜利70周年红场阅兵彩排",
                    "type": "1",
                    "img": [
                        "http://192.168.1.12/123456/1.jpg",
                        "http://192.168.1.12/123456/2.jpg" 
                    ]
                },
                {
                    "vid": "XOTQ5NTUyNzY4",
                    "url": "http://192.168.16.156:6789/open_video/la.mp4",
                    "title": "视频: 实拍老鹰抓小鸡幼崽 反遭母鸡反扑压身下",
                    "category": "快看",
                    "tag": "老人|收费站|插队",
                    "pub_time": "2015-01-24 06:10:19",
                    "description": "实拍老鹰抓小鸡幼崽 反遭母鸡反扑压身下 ",
                    "type": "2",
                    "img": [
                        "http://192.168.1.12/333444/1.jpg",
                        "http://192.168.1.12/333444/2.jpg" 
                    ]
                }
            ],
            "time": "2014-09-24 07:00:00",
            "key": "04e64625040a45d0ae621182546c770e" 
        }
    hc = HttpClient()
    res = hc.post_data('http://192.168.16.156:8990/op/push', json.dumps(content))
    if res:
        log.app_log.debug("return %s: %s" % (res[0], res[1]))

    '''
    content = {"origin": "upload", "describe": "1414", "uid": 1, "vid": "XNzIxNzUyMDAw", "title": u"侣行 第二季", "tags": u"t|a|g", "site": "cntv", "priority": 7, "channel":u"综艺|大陆|旅游|生活|真人秀|优酷出品"}
    hc = HttpClient()
    res = hc.post_data('http://192.168.16.118:6813/maze/addtask', json.dumps(content))
    if res:
        log.app_log.debug("return %s: %s" % (res[0], res[1]))
    '''
