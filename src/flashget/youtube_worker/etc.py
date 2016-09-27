#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    Global conf for provider server
"""
import time
import os

master_ip           = "111.161.35.220"
master_port         = "8090"
UGC_FILE_PATH       = "/ugc-data/upload_files/"
LOGPATH = "./"
MAX_FILE_NUM        = "10"
DATA_URL            = "http://111.161.35.219:7777/upload/download/?filename="
DATA_PATH           = "/flashget_data/"
op                  = "cu"#ct(dianxing),cu(liantong)
data_file           = "/youtube_worker/data.txt"
retry_num           = 10
time_out            = 3600#seconds
