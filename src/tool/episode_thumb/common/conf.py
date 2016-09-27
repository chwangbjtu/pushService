from tornado import options
from tornado import log
import sys
sys.path.append('.')
import os

class Conf(object):
    # proxy
    options.define('proxy_server', type=str)    

    # log
    #options.define('log_file_max_size', type=int)
    #options.define('log_file_prefix', type=str)
    
    # download
    options.define('download_host', type=str)
    options.define('download_username', type=str)
    options.define('download_password', type=str)
    options.define('download_directory', type=str)

    # database
    options.define('db_host', type=str)
    options.define('db_port',type=int)
    options.define('db_name', type=str)
    options.define('db_user', type=str)
    options.define('db_password', type=str)

    options.parse_config_file('ds.conf')

    proxy_server = options.options.proxy_server

    logging             = options.options.logging
    log_file_max_size   = options.options.log_file_max_size
    log_file_prefix     = options.options.log_file_prefix
    log_file_num_backups= options.options.log_file_num_backups
    log_to_stderr       = options.options.log_to_stderr

    download_host       = options.options.download_host
    download_username   = options.options.download_username
    download_password   = options.options.download_password
    download_directory  = options.options.download_directory
    youku_directory     = os.path.join(download_directory, 'youku')
    youtube_directory   = os.path.join(download_directory, 'youtube')
    iqiyi_directory     = os.path.join(download_directory, 'iqiyi')

    db_host     = options.options.db_host
    db_port     = options.options.db_port
    db_name     = options.options.db_name
    db_user     = options.options.db_user
    db_password = options.options.db_password

if __name__ == "__main__":
   
    conf = Conf()
    log.app_log.debug('proxy_server: %s' % conf.proxy_server)

    log.app_log.debug('logging: %s' % conf.logging)
    log.app_log.debug('log_file_max_size: %s' % conf.log_file_max_size)
    log.app_log.debug('log_file_num_backups: %s' % conf.log_file_num_backups)

    log.app_log.debug('download_host: %s' % conf.download_host)
    log.app_log.debug('download_username: %s' % conf.download_username)
    log.app_log.debug('download_password: %s' % conf.download_password)
    log.app_log.debug('download_directory: %s' % conf.download_directory)

    log.app_log.debug('db_host: %s' % conf.db_host)
    log.app_log.debug('db_port: %s' % conf.db_port)
    log.app_log.debug('db_name: %s' % conf.db_name)
    log.app_log.debug('db_user: %s' % conf.db_user)
    log.app_log.debug('db_password: %s' % conf.db_password)
