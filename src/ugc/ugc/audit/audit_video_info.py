import video_base
from audit_mgr import audit_mgr
from audit_mgr import constant
import json

class FunshionInfo(object):
    def __init__(self):
        self.funshion_id = ""
        self.rate = ""
        self.file_size = 0
        self.filename = ""
        self.duration = 0
        self.video_url = ""
        self.small_image = ""
        self.large_image = ""
        self.logo = ""
        self._audit_inst = audit_mgr.AuditMgr.instance()


class AuditVideoInfo(video_base.VideoBase):
    def __init__(self):
        self.funshion_list = {}
        self._audit_funshion = FunshionInfo()



if __name__ == "__main__":
    '''
    funsh_ins = FunshionInfo()
    uid = 1
    tid =  '222'
    if funsh_ins.get_funshion_info(tid):
        funsh_ins._sprintf()
    else:
        print 'not get the funshioninfo.'
    '''

    #tid = '222'
    #auditinfo =  AuditVideoInfo()
    #ret = auditinfo.process_video_info(tid)
    #if ret == None:
    #    print 'get none'
    #else:
    #    print 'ok.'
  