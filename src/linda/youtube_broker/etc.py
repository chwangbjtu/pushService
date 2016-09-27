#!/usr/bin/python
# -*- coding:utf-8 -*- 
download_path = "/data/"
redownload_num = 10
service_port = 9999
#[master]
#master_domain = "127.0.01:6809"
master_domain = "59.172.252.67:8190"
htbt_interval = 15
pull_task_interval = 10
report_task_interval = 1
#[sync]
resync_num = 10
sync_timeout = 3600#seconds
sync_master_info="rsync://linda@59.172.252.67:22221/ugc/"
sync_master_password_file = "/youtube_broker/rt/rsync.passwd"

