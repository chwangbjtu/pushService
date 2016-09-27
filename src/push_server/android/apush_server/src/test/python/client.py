import errno
import socket
from threading import Thread
from tornado import ioloop
from handler import ApushHandler

class Client(object):
    """
    The TCP Client class
        c = Client("test.myhost.com", 4242)
        c.start()
    """
    def __init__(self, host, port):
        self.read_chunk_size = 10240
        self.host = host
        self.port = port
        self.io_loop = ioloop.IOLoop.instance()
        self.finished = False
        self._handler = None
        
    def regist_handler(self, handler):
        self._handler = handler

    def start(self):
        # 1. establish a TCP connection to the flock server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.host, self.port))
        self.sock.setblocking(0)

        # 2. add to tornado for receiving a callback when we receive data
        self.io_loop.add_handler(
            self.sock.fileno(), self._handle_events, self.io_loop.ERROR)
        self.io_loop.update_handler(self.sock.fileno(), self.io_loop.READ)

        # 3. client callback
        if self._handler:
            connct_data = self._handler.get_connected_msg()
            self.sock.send(connct_data)

    def _handle_events(self, fd, events):
        if not self.sock:
            print "Got events for closed stream %d" % fd
            return
        if events & self.io_loop.READ:
            self._handle_read()
        if events & self.io_loop.ERROR:
            self._close_socket()
            return

    def _close_socket(self):
        try:
            self.io_loop.remove_handler(self.sock.fileno())
        except:
            pass

        if self.sock:
            self.sock.close()
            self.sock = None

    def _handle_read(self):
        """Signal by epoll: data chunk ready to read from socket buffer."""
        try:
            chunk = self.sock.recv(self.read_chunk_size)
        except socket.error, e:
            if e[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                return
            else:
                print "Read error on %d: %s" % (self.fileno, e)
                self._close_socket()
                return

        # empty data means closed socket per TCP specs
        if not chunk:
            self._close_socket()
            return

        # Print response
        # print "[%s:%s] chunk: %s" % (self.host, self.port, repr(chunk))
        if self._handler:
            self._handler.parse_msg(chunk, self.sock)


def main():        
    try:
        targets = ("192.168.16.155", 80)
        handler = ApushHandler()
        print "server ip, port: %s:%s" % (targets[0], targets[1])
        c = Client(targets[0], targets[1])
        c.regist_handler(handler)
        c.start()   
        io_loop = ioloop.IOLoop.instance()
        io_loop.start()
    except Exception as e:
        raise e


if __name__ == "__main__":
	main()