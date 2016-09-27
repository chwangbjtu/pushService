#-*- coding: utf-8 -*-
import datetime
import sys
import struct
import etc
import binascii
from connection import *

class APNSFeedbackWrapper(object):
    sandbox = True
    feedbacks = None
    connection = None

    def __init__(self, certificate = None, sandbox = True):
        self.connection = APNSConnection(certificate = certificate)
        self.sandbox = sandbox
        self.feedbacks = []

    def receive(self):
        self.feedbacks = []
        apns_connection = self.connection
        if self.sandbox != True:
            apnsHost = etc.APNS_FEEDBACK_HOST
        else:
            apnsHost = etc.APNS_FEEDBACK_SANDBOX_HOST

        apns_connection.connect(apnsHost, etc.APNS_FEEDBACK_PORT)

        while True:
            if len(self.feedbacks) > 10:
                break
                
            reply_buf = apns_connection.read(etc.APNS_FEEDBACK_BUFFER_SIZE)
            if reply_buf:
                reply_buf_length = len(reply_buf)
                if reply_buf_length == 0:
                    break
                
                while reply_buf_length >= etc.APNS_FEEDBACK_BLOCK_SIZE:
                    reply_block = reply_buf[0 : etc.APNS_FEEDBACK_BLOCK_SIZE]
                    unpack_format = "!IH" + str(etc.APNS_FEEDBACK_TOKEN_LENGTH) + "s"
                    unpack_block = struct.unpack(unpack_format, reply_block)
                    if len(unpack_block) == 3:
                        token = binascii.b2a_hex(unpack_block[2])
                        self.feedbacks.append(token)
                    
                    reply_buf = reply_buf[etc.APNS_FEEDBACK_BLOCK_SIZE : ]
                    reply_buf_length = len(reply_buf)

        apns_connection.close()
        return self.feedbacks
