#!/usr/bin/python
# -*- coding:utf-8 -*- 
import ugc.settings as settings

host   = settings.DATABASES['default']['HOST']
user   = settings.DATABASES['default']['USER']
passwd = settings.DATABASES['default']['PASSWORD']
db     = settings.DATABASES['default']['NAME']
port   = int(settings.DATABASES['default']['PORT'])


SERVICE_PORT = '8778'

LOGPATH = './log/'

log_for_procedure = 'procedure_log'
error_for_procedure = 'procedure_error'

log_for_db_manager = 'db_manager_log'
error_for_db_manager = 'db_manager_error'

log_for_process = 'process_log'
error_for_process = 'process_error'

apply_task = 'proc_apply_task'
page_task = 'proc_page_task'


verify_report = '/api/?cmd=upload_data&cli=upload_verify_data'

verify_hash = '/api/?cmd=upload_hash_data&cli=upload_verify_hash'

verify_exam = '/crane/?cmd=examresult'

verify_hash_dat = '/api/?cmd=upload_hash_info&cli=upload_verify_hash_dat'



