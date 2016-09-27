from multiprocessing import Process, Manager, Lock
import time

class MemQueue(object):
    def __init__(self, qname):
        self._queue = Manager().list()
        self._lock = Lock()
        self._qname = qname
        self._index = 0

    def __iter__(self):
        return self

    def next(self):
        with self._lock:
            try:
                result = self._queue[self._index]
            except IndexError:
                raise StopIteration
            self._index += 1
            return result

    def ping(self):
        return True

    def add_tail(self, ep):
        with self._lock:
            self._queue.append(ep)
    
    def add_head(self, ep):
        with self._lock:
            self._queue.insert(0, ep)
    
    def remove(self, ep):
        with self._lock:
            self._queue.remove(ep)

    def pop_head(self):
        with self._lock:
            if len(self._queue) > 0:
                return self._queue.pop(0)

    def pop_tail(self):
        with self._lock:
            if len(self._queue) > 0:
                return self._queue.pop()

    def size(self):
        with self._lock:
            return len(self._queue)

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
            
    _q = MemQueue()
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
