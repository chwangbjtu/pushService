# -*-coding:utf-8 -*-
from tornado import log
from tornado import options

class Conf(object):
    #tornado server
    options.define('server_port', type=int)

    #mysql for old management
    options.define('sql_host', type=str)
    options.define('sql_port', type=int)
    options.define('sql_user', type=str)
    options.define('sql_passwd', type=str)
    options.define('sql_db', type=str)

    #token mongodb for device token
    options.define('mg_urls', type=str)
    options.define('mg_db', type=str)
    options.define('mg_user', type=str)
    options.define('mg_passwd', type=str)

    #get task hanlder
    options.define('pull_number', type=int)
    options.define('token_basic_number', type=int)

    #push server port
    options.define('push_server_port', type=int)

    #progress
    options.define('progress_interval_time', type=int)
    options.define('progress_expire_time', type=int)
    
    #msg redis for push message
    options.define('rs_host', type=str)
    options.define('rs_port', type=int)
    options.define('rs_passwd', type=str)
    #msg redis sentinel for push message
    options.define('sntl_urls', type=str)
    options.define('sntl_passwd', type=str)
    options.define('sntl_master_name', type=str)
    #msg redis for push message
    options.define('msg_expire_time', type=int)
    options.define('msg_stat_expire_time', type=int)
    options.parse_config_file('is.conf')

    #tornado server
    server_port = options.options.server_port

    #mysql for old management
    sql_host = options.options.sql_host
    sql_port = options.options.sql_port
    sql_user = options.options.sql_user
    sql_passwd = options.options.sql_passwd
    sql_db = options.options.sql_db

    #token mongodb for device token
    mg_urls = options.options.mg_urls
    mg_db = options.options.mg_db
    mg_user = options.options.mg_user
    mg_passwd = options.options.mg_passwd

    #get task handler
    pull_number = options.options.pull_number
    token_basic_number = options.options.token_basic_number

    #push server port
    push_server_port = options.options.push_server_port

    #progress
    progress_interval_time = options.options.progress_interval_time
    progress_expire_time = options.options.progress_expire_time

    #msg redis for push message
    rs_host = options.options.rs_host
    rs_port = options.options.rs_port
    rs_passwd = options.options.rs_passwd
    #msg redis sentinel for push message
    sntl_urls = options.options.sntl_urls
    sntl_passwd = options.options.sntl_passwd
    sntl_master_name = options.options.sntl_master_name
    #msg redis for push message
    msg_expire_time = options.options.msg_expire_time
    msg_stat_expire_time = options.options.msg_stat_expire_time

if __name__ == "__main__":
    conf = Conf()
