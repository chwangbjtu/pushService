# -*-coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.')
from common.util import NodeType
from common.node_manager import NodeManager

class AddNodeHandler(object):

    def __init__(self):
        self.__node_manager = NodeManager()

    def handle(self, para=None, body=None):
        result = ''
        try:
            if not body:
                return result
            body_json = json.loads(body)
            if self.add_node(body_json):
                res = {}
                res['retcode'] = '200'
                res['retmsg'] = 'ok'
                result = json.dumps(res)
                return result
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            if not result:
                res = {}
                res['retcode'] = '404'
                res['retmsg'] = 'not found'
                result = json.dumps(res)
            return result

    def add_node(self, node):
        res = False
        try:
            node = node['node'] if 'node' in node else []
            if not node:
                return res
            for n in node:
                type = n['type'] if 'type' in n else ''
                ip = n['ip'] if 'ip' in n else ''
                if type and ip:
                    if type == NodeType.Push:
                        if not self.__node_manager.update_or_insert_node(type, ip):
                            return
            res = True
        except Exception, e:
            res = False
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res
