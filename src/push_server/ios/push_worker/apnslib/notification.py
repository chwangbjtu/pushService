#-*- coding: utf-8 -*-
from apnsexceptions import *
import struct
import binascii
import etc
import time
import json
from tornado import log

NULL = 'null'

class APNSAlert(object):
    def __init__(self):
        self.alert_header = None
        self.alert_body = None
        self.action_loc_key = None
        self.loc_key = None
        self.loc_args = None
        
    def set_header(self, alert_header):
        if alert_header and not isinstance(alert_header, str) and not isinstance(alert_header, unicode):
            raise APNSValueError, "Unexpected value of argument. It should be string or None."

        self.alert_header = alert_header
        return self
    
    def set_body(self, alert_body):
        if alert_body and not isinstance(alert_body, str) and not isinstance(alert_body, unicode):
            raise APNSValueError, "Unexpected value of argument. It should be string or None."

        self.alert_body = alert_body
        return self
    
    def set_action_loc_key(self, alk = NULL):
        if alk and not isinstance(alk, str) and not isinstance(alk, unicode):
            raise APNSValueError, "Unexpected value of argument. It should be string or None."

        self.action_loc_key = alk
        return self

    def set_loc_key(self, lk):
        if lk and not isinstance(lk, str) and not isinstance(lk, unicode):
            raise APNSValueError, "Unexpected value of argument. It should be string or None"
        self.loc_key = lk
        return self

    def set_loc_args(self, la):
        if la and not isinstance(la, (list, tuple)):
            raise APNSValueError, "Unexpected type of argument. It should be list or tuple of strings"

        self.loc_args = la
        return self

    def build_param(self):
        arguments = {}
        if self.alert_header:
            arguments['title'] = self.alert_header
            
        if self.alert_body:
            arguments['body'] = self.alert_body

        if self.action_loc_key:
            arguments['action-loc-key'] = self.action_loc_key

        if self.loc_key:
            arguments['loc-key'] = self.loc_key

        if self.loc_args:
            arguments['loc-args'] = self.loc_args

        return arguments
        
class APNSProperty(object):
    name = None
    data = None
    def __init__(self, name = None, data = None):
        if not name or not isinstance(name, str) or len(name) == 0:
            raise APNSValueError, "Name of property argument should be a non-empry string"
        if not isinstance(data, (int, str, list, tuple, float,dict)):
            raise APNSValueError, "Data argument should be string, number, list of tuple"

        self.name = name
        self.data = data

    def build_param(self):
        arguments = {}
        arguments['name'] = self.name
        arguments['data'] = self.data
        
        return arguments

class APNSNotification(object):  
    command = 2
    max_payload_length = 2048
    device_token_length = 32

    def __init__(self):
        self.properties = []
        self.badge_value = None
        self.sound_value = None
        self.alert_object = None
        self.device_token = None
        self.expire_date = int(time.time()) + 3600
        self.identifier = 0
        self.priority = 10

    def get_token(self):
        return binascii.b2a_hex(self.device_token)

    def token_base64(self, encoded_token):
        self.device_token = base64.standard_b64decode(encoded_token)
        return self

    def token_hex(self, hex_token):
        hex_token = hex_token.strip().strip('<>').replace(' ','').replace('-', '')
        self.device_token = binascii.a2b_hex(hex_token)
        return self

    def badge(self, num = None):
        if num == None:
            self.badge_value = None
            return self

        if not isinstance(num, int):
            raise APNSValueError, "Badge argument must be a number"
        self.badge_value = num
        return self

    def sound(self, sound = 'default'):
        if sound == None:
            self.sound_value = None
            return self
            
        self.sound_value = str(sound)
        return self

    def alert(self, alert = None):
        if not isinstance(alert, str) and not isinstance(alert, unicode) and not isinstance(alert, APNSAlert):
            raise APNSTypeError, "Wrong type of alert argument. Argument should be String, Unicode string or an instance of APNSAlert object"
            
        self.alert_object = alert
        return self
    
    def expire(self, expire_date):
        if not isinstance(expire_date, int):
            raise APNSValueError, "expire argument must be a number"
            
        self.expire_date = expire_date
        return self
        
    def identify(self, identifier):
        if not isinstance(identifier, int):
            raise APNSValueError, "identify argument must be a number"
            
        self.identifier = identifier
        return self
        
    def priority(self, priority):
        if not isinstance(priority, int):
            raise APNSValueError, "priority argument must be a number"
            
        self.priority = priority
        return self

    def append_property(self, *args):
        for prop in args:
            if not isinstance(prop, APNSProperty):
                raise APNSTypeError, "Wrong type of argument. Argument should be an instance of APNSProperty object"
                
            self.properties.append(prop)
            
        return self

    def clear_properties(self):
        self.properties = None

    def build_param(self):
        keys = {}
        apsKeys = {}
        if self.sound_value:
            apsKeys['sound'] = self.sound_value

        if self.badge_value:
            apsKeys['badge'] = self.badge_value

        if self.alert_object != None:
            apsKeys['alert'] = self.alert_object.build_param()

        keys['aps'] = apsKeys
        # prepare properties
        for property in self.properties:
            param = property.build_param()
            keys[param['name']] = param['data']

        payload = json.dumps(keys)
        # remove ' '
        payload = ''.join(payload.split())
        log.app_log.info(payload)
        if len(payload) > self.max_payload_length:
            raise APNSPayloadLengthError, "Length of Payload more than %d bytes." % self.max_payload_length

        return payload

    def payload(self):
        if self.device_token == None:
            raise APNSUndefinedDeviceToken, "You forget to set device_token in your notification."

        payload = self.build_param()
        payload_length = len(payload)
        
        token_item_format = "!BH" + str(self.device_token_length) + "s"
        token_item = struct.pack(token_item_format, etc.DEVICE_TOKEN_ID, self.device_token_length, self.device_token)
        
        payload_item_format = "!BH" + str(payload_length) + "s"
        payload_item = struct.pack(payload_item_format, etc.PAYLOAD_ID, payload_length, payload)
        
        identifier_item = expire_date_item = priority_item = ''
        identifier_item_format = "!BHI"
        identifier_item = struct.pack(identifier_item_format, etc.NOTIFICATION_IDENTIFIER_ID, 4, self.identifier)
    
        expire_date_item_format = "!BHI"
        expire_date_item = struct.pack(expire_date_item_format, etc.EXPIRATION_DATE_ID, 4, self.expire_date)
    
        priority_item_format = "!BHB"
        priority_item = struct.pack(priority_item_format, etc.PRIORITY_ID, 1, self.priority)
        
        total_len = len(token_item) + len(payload_item) + len(identifier_item) + len(expire_date_item) + len(priority_item)
        total_item = token_item + payload_item + identifier_item + expire_date_item + priority_item
        
        items_format = "!BI" + str(total_len) + "s"
        return struct.pack(items_format, self.command, total_len, total_item)
        