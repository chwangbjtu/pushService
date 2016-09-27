
from audit_mgr import audit_mgr
from audit_mgr import constant
import json

class VideoBase(object):
    def __init__(self):
        self.tid = ""
        self.site = ""
        self.title = ""
        self.tags = ""
        self.origin = ""
        self.channel = ""
        self.description = ""
        self.priority = None
        self.step = ""
        self.status = None
        self.video_id = ""
        self.seconds = None
        self.ttype = None
        self.user = ""

    def normalize(self):
        pass
