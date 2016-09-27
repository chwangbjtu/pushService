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

class RedisQueue(object):
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
            self._inst.lpush(self._qname, json.dumps(ep, cls=ComplexEncoder))
            #self._inst.lpush(self._qname, json.dumps(ep, cls=DateTimeAwareJSONEncoder))
    
    def add_tail(self, ep):
        with self._lock:
            self._inst.rpush(self._qname, json.dumps(ep, cls=ComplexEncoder))

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
            item = self._inst.rpop(self._qname)
            if item:
                ep  = json.loads(item)
                #ep  = json.loads(item, cls=DateTimeAwareJSONDecoder)
                return ep

    def size(self):
        with self._lock:
            return self._inst.llen(self._qname)

    def clear(self):
        with self._lock:
            self._inst.delete(self._qname)

if __name__ == "__main__":

    def produce(q):
        for i in xrange(200):
            print 'p: %s' % i
            q.add_tail(i)
            time.sleep(0.1)

    def consume(q, index):
        while True:
            print 'c%s: %s' % (index, q.pop_tail())
            time.sleep(1)
            
    _q = RedisQueue()
    if _q.ping():
        p1 = Process(target=produce, args=(_q,))
        c1 = Process(target=consume, args=(_q, 1))
        c2 = Process(target=consume, args=(_q, 2))
        c3 = Process(target=consume, args=(_q, 3))
        p1.start()
        c1.start()
        c2.start()
        c3.start()
        p1.join()
        c1.join()
        c2.join()
        c3.join()
    else:
        print 'cannot connect to redis'
