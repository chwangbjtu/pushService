# -*- coding:utf-8 -*-
"""
    Global conf for provider server
"""
import time
import os

data_path       = "/flashget_data/video/"
retry_num       = 2
master_ip       = "111.161.35.220"
#master_port     = 6807
master_port     = 8090
url_path        = "http://111.161.35.220:9438/video/"
op              = "cu"#ct/cu
sites           = '{"yk":"http://v.youku.com/v_show/id_","qy":"http://www.iqiyi.com/","pptv":"","funshion":"","k6":"k6","56":"56","qq":"qq","kuaikan":"kuaikan"}'
other_sites     = '{"test":""}'
special_flv     = '{"qy":"qy"}'
data_file       = "/flashget/flashget_worker/data.txt"
mp4box_dir      = "/flashget/flashget_worker/mp4box"
flv_project_dir = "/flashget/flashget_worker/flv_project"
