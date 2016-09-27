#-*- coding: utf-8 -*-
import os
import socket
import time
import etc

from socket import socket, AF_INET, SOCK_STREAM
try:
    from ssl import wrap_socket
except ImportError:
    from socket import ssl as wrap_socket

from apnsexceptions import *

class APNSConnection(object):
    certificate = None
    host = None
    port = None
    def __init__(self, certificate = None):
        self.certificate = certificate
        
        path = os.path.join(os.path.dirname(__file__), "key")
        self._key = path + "/" + certificate + "_key.pem"
        self._cert = path + "/" + certificate + "_cert.pem"

    def connect(self, host, port):
        self.host = host
        self.port = port

    def write(self, data = None):
        buf = None
        _socket = None
        try:
            _socket = socket(AF_INET, SOCK_STREAM)
            _socket.connect((self.host, self.port))
            _ssl = wrap_socket(_socket, self._key, self._cert)
            _ssl.write(data)
            #_socket.setblocking(0)
            
            _socket.settimeout(etc.APNS_READ_WAIT)
            buf = _ssl.read(etc.APNS_READ_BUF_SIZE)
            if _socket:
                _socket.close()
        
        except Exception, e:
            pass
            
        finally:
            if _socket:
                _socket.close()
        
        return buf
    
    def read(self, buf_len):
        buf = None
        _socket = None
        try:
            _socket = socket(AF_INET, SOCK_STREAM)
            _socket.settimeout(5)
            _socket.connect((self.host, self.port))
            _ssl = wrap_socket(_socket, self._key, self._cert)      
            buf = _ssl.read(buf_len)
        
        except Exception, e:
            pass
            
        finally:
            if _socket:
                _socket.close()
        
        return buf

    def close(self):
        pass
