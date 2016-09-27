#!/usr/bin/python
# -*- coding:utf-8 -*-
host = '192.168.16.156'
user = 'root'
passwd = 'root'
db = 'yumei_ugc'
port = 3306

MAZE_IP = '192.168.16.156'
SERVICE_PORT = 6808
pid = '/home/spider/maze_service/mazed.pid'
DBPATH = "/home/spider/maze_service"
DATABASENAME = DBPATH + "status_report.db"
FORWARDS_TASK_DB = DBPATH + "forwardsdoor.db"
LOGPATH = "/home/spider/maze_service/"
MAX_LOGFILE_SIZE = 50 #M

LOG_FOR_HTTP_IO       = 'http_io'
ADD_TASK_LOG          = "add_task"
STATUS_REPORT_LOG     = "status_report"
GET_TASK_LOG          = "get_task"
LOG_FOR_VERIFY        = "verify_crane"
LOG_FOR_NOTIFY_QIYI   = 'qiyi_process'
LOG_FOR_PROCEDURE     = 'db_procedure'
LOG_FOR_DB_MGR        = 'db_manager'
SEND_FOR_MACROS       = 'macros_send'
TASKQUEUE             = "taskqueue"
NOTIFY_PACK           = "notify_pack"
EXCEPT_THROW          = "except_error"
URLERROR              = "url_error"
PROCESSERROR          = "process_error"
CLOUDID_TIDMAP        = "cloud_taskid_map"

apply_task            = 'proc_apply_task'
page_task             = 'proc_page_task'

verify_report   = '/api/?cmd=upload_data&cli=upload_verify_data'
verify_hash     = '/api/?cmd=upload_hash_data&cli=upload_verify_hash'
verify_exam     = '/crane/?cmd=examresult'
verify_hash_dat = '/api/?cmd=upload_hash_info&cli=upload_verify_hash_dat'

cloud_add_taskmap        = '/maze/report_cloud_id'          # 保存taskid与tid对应关系接口
cloud_get_tasklist       = '/maze/get_tasklist'             # 获取批量任务
cloud_transcode_report   = '/maze/cloud_transcode_report'   # service，转码信息上报接口url
cloud_notify_pack_dat    = '/notify_pack_dat/'              # 云转码服务接口url
cloud_notify_loaded_info = '/maze/cloud_loaded_report'      # service,打包加载信息上报接口url
cloud_delete_task        = '/notify_delete_task/'           # 删除任务

macros_ip      = 'macross.funshion.com:27777'
macros_method  = '/api/?cmd=report_video&cli=ugc&user_name=ugc'

CLOUD_SERVICE_IP       = 'centaurus.funshion.com'
CLOUD_SERVICE_PORT     = 6531  #cloud service port.
CLOUD_SERVICE_ADD_TASK = "/add_task"

DELETE_TASK            = "cloud_delete_task"
_ADD_TASK_STATUS       = "/maze/addstatus"
_GET_TASK_STATUS       = "/maze/getstatus"
_ADD_VIDEO_URL         = "/maze/upload_url"
_URL_MAZE_POST_TASK    = "/maze/addtask"
_URL_MAZE_POST_AUDIT   = "/maze/audit"
_MAZE_QUERY_INFO       = "/maze/queryinfo"
_MAZE_2MACROS_INFO     = "/maze/macrosinfo"

CLOUD_TASK_DEL_DAYS = 1

URGENT_USER = [ 1 ]
TRANSCODE_FREE = 0 
MASAIC_FREE = 0
LOGO_FREE = 0
