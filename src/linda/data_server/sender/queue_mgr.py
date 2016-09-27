import sys
sys.path.append('.')
from common.conf import Conf
from mem_queue import MemQueue
from redis_queue_priority import RedisQueuePriority
import time

class QueuesManager(object):

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self, storage=None):
        self.storage = storage
        self.queues = { \
                        'mz_q': self.create_queue('mz_q'), \
                       }

    def create_queue(self, qname):
        if Conf.enable_redis:
            return RedisQueuePriority(qname)

        return MemQueue(qname)


    def get_queue(self, queue_name):
        queue = None
        if queue_name in self.queues:
            queue = self.queues[queue_name]

        return queue

if __name__ == "__main__":

    from multiprocessing import Process, Lock

    def consume(mgr, q_name):
        while True:
            q = mgr.get_queue(q_name)
            print 'c%s: %s' % (q_name, q.pop_tail())
            time.sleep(1)
            
    mgr = QueuesManager.get_instance()
    c1 = Process(target=consume, args=(mgr, 'mz_q'))
    c2 = Process(target=consume, args=(mgr, 'ep_q'))

    c1.start()
    c2.start()
