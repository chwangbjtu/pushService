#-*- coding: utf-8 -*-
from __init__ import *
from connection import *
from tornado import log
import traceback
import etc
from statistics import Statistics
from tokens import TokenMgr

class APNSNotificationWrapper(object):
    sandbox = True
    payloads = None
    connection = None
    identifier = 1
    error_at = 0

    def __init__(self, certificate = None, sandbox = True):
        self.connection = APNSConnection(certificate = certificate)
        self.sandbox = sandbox
        self.payloads = []
        
    def append(self, payload = None):
        if not isinstance(payload, APNSNotification):
            raise APNSTypeError, "Unexpected argument type. Argument should be an instance of APNSNotification object"
        payload.identify(self.identifier)
        self.payloads.append(payload)
        self.identifier += 1

    def count(self):
        return len(self.payloads)
        
    def add_failed_num(self):
        statistics_obj = Statistics()
        statistics_obj.add_failed_num()

    def clear(self):
        self.identifier = 1
        self.error_at = 0
        self.payloads = []
        
    def notify(self):
        payloads = [o.payload() for o in self.payloads]
        messages = []

        if len(payloads) == 0:
            return False

        for p in payloads:
            plen = len(p)
            messages.append(struct.pack('%ds' % plen, p))

        message = "".join(messages)
        apnsConnection = self.connection
        if self.sandbox != True:
            apns_host = etc.APNS_HOST
        else:
            apns_host = etc.APNS_SANDBOX_HOST
        apnsConnection.connect(apns_host, etc.APNS_PORT)
        buf = apnsConnection.write(message)
        apnsConnection.close()
        if buf:
            log.app_log.info("error occured")
            self.add_failed_num()
            self.error_handler(buf)
        
        return True
    
    def error_handler(self, buf):
        try:         
            unpack_buf = struct.unpack("!BBI", buf)
            if len(unpack_buf) == 3:
                log.app_log.info("error :%s", unpack_buf)
                error_at = unpack_buf[2]
                error_no = unpack_buf[1]
                start = error_at - self.error_at
                
                if error_no == etc.SHUTDOWN or error_no == etc.NO_ERROR_HAPPENED or error_no == etc.PROCESSING_ERROR:
                    #start = start - 1
                    pass
                else:
                    if error_no == etc.INVALID_TOKEN:     
                        error_payload = self.payloads[start - 1]
                        error_token = error_payload.get_token()
                        log.app_log.info("invalid token:%s", error_token)
                        
                        token_mgr = TokenMgr()
                        token_mgr.add_delete_token(error_token)
                    
                self.payloads = self.payloads[start:]
                self.error_at = error_at
                self.notify()
                
        except Exception, e:
            pass
            
