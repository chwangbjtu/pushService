# -*-coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.') 
from conf import Conf 
from service.pull_service import PullService

class GetTaskHandler(object):

    def __init__(self):
        self.__pull_service = PullService()

    def handle(self, para=None, body=None):
        result = ''
        try:
            if para:
                pull_number = para['total'] if 'total' in para else Conf.pull_number 
            if not pull_number:
                pull_number = Conf.pull_number 
            pull_number = int(pull_number)
            if pull_number % Conf.token_basic_number != 0:
                log.app_log.info('pull_number(%s) is invalid' % pull_number)
                return
            res = self.__pull_service.get_task(pull_number)
            if res:
                res['retcode'] = '200'
                res['retmsg'] = 'ok'
                result = json.dumps(res)
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            if not result:
                res = {}
                res['retcode'] = '404'
                res['retmsg'] = 'not found'
                result = json.dumps(res)
            return result
