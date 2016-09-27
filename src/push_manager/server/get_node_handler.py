# -*-coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.')
from common.node_manager import NodeManager

class GetNodeHandler(object):

    def __init__(self):
        self.__node_manager = NodeManager()

    def handle(self, para=None, body=None):
        result = ''
        try:
            type = para['type'] if 'type' in para else ''
            node = self.get_node(type)
            if node:
                res = {}
                res['retcode'] = '200'
                res['retmsg'] = 'ok'
                res['node'] = node
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

    def get_node(self, type):
        res = []
        try:
            res= self.__node_manager.findmany_node(type=type)
        except Exception, e:
            res = []
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res
