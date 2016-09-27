from multiprocessing import Process, Lock
import time
import redis
import json
from datetime import datetime

import sys
sys.path.append(".")
from common.conf import Conf

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class DateTimeAwareJSONEncoder(json.JSONEncoder):
    """ 
    Converts a python object, where datetime and timedelta objects are converted
    into objects that can be decoded using the DateTimeAwareJSONDecoder.
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__' : 'datetime',
                'year' : obj.year,
                'month' : obj.month,
                'day' : obj.day,
                'hour' : obj.hour,
                'minute' : obj.minute,
                'second' : obj.second,
                'microsecond' : obj.microsecond,
            }   

        elif isinstance(obj, timedelta):
            return {
                '__type__' : 'timedelta',
                'days' : obj.days,
                'seconds' : obj.seconds,
                'microseconds' : obj.microseconds,
            }   

        else:
            return json.JSONEncoder.default(self, obj)

class DateTimeAwareJSONDecoder(json.JSONDecoder):
    """ 
    Converts a json string, where datetime and timedelta objects were converted
    into objects using the DateTimeAwareJSONEncoder, back into a python object.
    """

    def __init__(self, *args, **kargs):
            json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)

    def dict_to_object(self, d): 
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        if type == 'datetime':
            return datetime(**d)
        elif type == 'timedelta':
            return timedelta(**d)
        else:
            # Oops... better put this back together.
            d['__type__'] = type
            return d

class RedisQueuePriority(object):
    def __init__(self, qname):
        self._lock = Lock()
        self._qname = qname
        self._inst = redis.StrictRedis(host=Conf.redis_host, port=Conf.redis_port)

    def ping(self):
        with self._lock:
            try:
                return self._inst.ping() 
            except redis.exceptions.ConnectionError:
                return False

    def add_head(self, ep):
        with self._lock:
            data = ep.get('data')
            if data:
                priority = data.get('priority',1)
            self._inst.zadd(self._qname, priority,json.dumps(ep, cls=ComplexEncoder))

    def remove(self, ep):
        with self._lock:
            self._inst.lrem(self._qname, 0, ep)

    def pop_head(self):
        with self._lock:
            item = self._inst.lpop(self._qname)
            if item:
                ep  = json.loads(item)
                return ep

    def pop_tail(self):
        with self._lock:
            item = self._inst.zrevrange(self._qname,0,0)
            #item = self._inst.rpop(self._qname)
            if item:
                item = item[0].strip()
                ep  = json.loads(item)
                #ep  = json.loads(item, cls=DateTimeAwareJSONDecoder)
                self._inst.zrem(self._qname,item)
                return ep

    def size(self):
        with self._lock:
            return self._inst.llen(self._qname)

    def clear(self):
        with self._lock:
            self._inst.delete(self._qname)

    def set_dispatch_per_minute(self, qdn):
        with self._lock:
            self._inst.set('query_dispatching_num', qdn)

    def get_dispatch_per_minute(self):
        with self._lock:
            return self._inst.get('query_dispatching_num')

if __name__ == "__main__":
    rq = RedisQueuePriority("test")
    '''
    rq.add_head({"priority":1,"test":"test"})
    rq.add_head({"priority":2,"test":"test"})
    rq.add_head({"priority":3,"test":"test"})
    rq.add_head({"priority":4,"test":"test"})
    rq.add_head({"priority":5,"test":"test"})
    rq.add_head({"priority":6,"test":"test"})
    rq.add_head({"priority":7,"test":"test"})
    '''
    #print rq.pop_tail()
    rq.set_dispatch_per_minute(1)
    print type(rq.get_dispatch_per_minute())
    print rq.get_dispatch_per_minute()
