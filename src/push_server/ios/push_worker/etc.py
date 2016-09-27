#-*- coding: utf-8 -*-

#thream manger
WORKER_NUM = 2
TASK_NUM = 100
TASK_LIST_MAX = 100
ERROR_WAIT_TIME = 5

#app name
IPHONE_CERT = "iphone"
IPAD_CERT = "ipad"
FUNSHIONTV_CERT = "funshionTV"
IPADPLAYERPLUS = "ipadplayerplus"
IPHONEPLAYERPLUS = "iphoneplayerplus"
CERT_LIST = [IPHONE_CERT, IPAD_CERT, FUNSHIONTV_CERT, IPADPLAYERPLUS, IPHONEPLAYERPLUS]

#error msg
TASK_FORMAT_ERROR = "task format error"
DEVICE_INFO_FORMAT_ERROR = "device_info format error"
MSG_INFO_FORMAT_ERROR = "msg_info format error"
DEVICE_INFO_MUST_BE_LIST = "device info must be list"
ALERT_MUST_BE_DICT = "alert must be dict"

#log
logging='INFO'
log_file_max_size = 100000000
log_file_prefix = 'log/ps.log'
log_file_num_backups=30

#server info
PUSH_SERVER_HOST = "192.168.16.165:8990"
DEVICE_MANAGER_HOST = '192.168.16.165:18000'
URL_TYPE = "http://"
TIME_OUT = 20

#feedback switch
open_feedback = 0
