#store ip:port/api/?cmd=upload_data&cli=upload_verify_data report data.
import json

class VerifyMsInfo(object):
    dat_infohash = ""
    dat_size  = 0
    ms_server_ip = ""
    ms_server_port = ""

    def  __init__(self):
        pass

    def serialization(self, json_info):
        try:
            if json_info == None:
                print 'the json_info is none.'
                return False
            self.dat_infohash = json_info['infohash']
            self.dat_size = int(json_info['size'])
            self.ms_server_ip = json_info['server_ip']
            self.ms_server_port = json_info['server_port']
            return True
        except Exception,e:
            print e
            return False