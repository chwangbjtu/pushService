#!/usr/bin/python
# -*- coding:utf-8 -*- 
import ugc.settings as settings

host   = settings.DATABASES['default']['HOST']
user   = settings.DATABASES['default']['USER']
passwd = settings.DATABASES['default']['PASSWORD']
db     = settings.DATABASES['default']['NAME']
port   = int(settings.DATABASES['default']['PORT']) 

MAZE_SERVICE_IP   = settings.MAZE_HOST
MAZE_SERVICE_PORT = int(settings.MAZE_PORT)

cloud_notify_loaded_info = '/maze/cloud_loaded_report'   #通知打包接口
cloud_notify_pack_dat = '/notify_pack_dat/'              #cloud service 

LOGPATH = './log/'

log_for_procedure = 'procedure_log'
error_for_procedure = 'procedure_error'

log_for_process = 'process_log'
error_for_process = 'process_error'

error_for_db_connect = "dbconnect_error"

apply_task = 'proc_apply_task_new'
page_task = 'proc_page_task'

status_service = 'http://%s:%d/maze/getstatus' % (MAZE_SERVICE_IP,MAZE_SERVICE_PORT)

CLOUD_SERVICE_IP   = settings.CLOUD_HOST
CLOUD_SERVICE_PORT = int(settings.CLOUD_PORT)


v_all_tasklist = ""

