# -*-coding:utf-8 -*- 
import protocol
import json
import time
import threading 

class HtbtThread(threading.Thread):
    def __init__(self, htbt, sock):
        threading.Thread.__init__(self)
        self._htbt = htbt
        self._sock = sock
        
    def run(self):
        htbt_msg = ""
        encryp_msg = protocol.build_msg(protocol.proto_htbt_req, htbt_msg)
        while True:
            self._sock.send(encryp_msg)
            time.sleep(self._htbt)

class ApushHandler(object):
    def __init__(self):
        self._last_msg_id = 240
        self._app_name = "aphone"
        self._mac = "78f5fd6d6d6f"
        self._token = "aacc"
        self._version = "2.6.1.0"
        self._htbt_thread = None
        
    def get_connected_msg(self):
        payload = {"app_name":self._app_name, "last_msg_id":str(self._last_msg_id), "mac":self._mac, "token":self._token, "version":self._version}
        msg = json.dumps(payload)
        print "login msg: ", msg
        encryp_msg = protocol.build_msg(protocol.proto_login_req, msg)
        return encryp_msg
        
    def parse_msg(self, msg, sock):
        result = protocol.parse_msg(msg)
        print "server response: ", result
        type = result['type']
        source = result['source']
        if type == protocol.proto_login_resp:
            return self.login_handler(source, sock)
        if type == protocol.proto_htbt_resp:
            return self.htbt_handler(source, sock)
        if type == protocol.proto_push_resp:
            return self.push_handler(source, sock)
        
    def login_handler(self, msg, sock):
        data = json.loads(msg)
        htbt = int(data['htbt'])
        
        if not self._htbt_thread:
            print "start heart beat thread!"
            self._htbt_thread = HtbtThread(htbt, sock)
            self._htbt_thread.start()
        
    def htbt_handler(self, msg, sock):
        print "heart beat response"
        
    def push_handler(self, msg, sock):
        push_msg = json.loads(msg)
        msgid = int(push_msg['msgid'])
        print "receive push msg:", msg
        response = json.dumps({"msgid":msgid})
        encryp_msg = protocol.build_msg(protocol.proto_push_req, response)
        sock.send(encryp_msg)
        
    