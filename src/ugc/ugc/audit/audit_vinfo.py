class AuditVInfo(object):
    def __init__(self):
        self.title = ""
        self.tags = ""
        self.channel = ""
        self.post_user = ""
        self.page_view = ""
        self.small_img_list = ""
        self.large_img = ""
        #0:to be audited;1: passed;2:killed
        self.state = None

    def normalize(self):
        self.small_img_list = []
        simg_url_list = self.small_img_list.split("|")
        if not simg_url_list:
            return
        for item in simg_url_list:
            if item:
                self.small_img_list.append(item)


