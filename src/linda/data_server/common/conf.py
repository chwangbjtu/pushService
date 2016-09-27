from tornado import options
from tornado import log

class Conf(object):
    options.define('server_port', type=int)    
    options.define('service_interval', type=int)    
    options.define('check_new_since', type=int)
    options.define('enable_blacklist',type=bool)
    options.define('db_host', type=str)
    options.define('db_port', type=int)
    options.define('db_name', type=str)
    options.define('db_user', type=str)
    options.define('db_password', type=str)
    options.define('linda_url', type=list)
    options.define('add_linda', type=str)
    options.define('linda_query_url', type=str)
    options.define('enable_redis',type=bool)
    options.define('redis_host', type=str)
    options.define('redis_port', type=int)
    options.define('max_retry', type=int)
    options.define('common_sleep_time', type=int)
    options.define('fail_sleep_time', type=int)
    options.define('busy_max_send_num', type=int)
    options.define('idle_max_send_num', type=int)
    options.define('linda_query_interval', type=int)

    options.parse_config_file('ds.conf')

    server_port = options.options.server_port
    service_interval = options.options.service_interval
    check_new_since = options.options.check_new_since
    enable_blacklist = options.options.enable_blacklist
    db_host = options.options.db_host
    db_port = options.options.db_port
    db_name = options.options.db_name
    db_user = options.options.db_user
    db_password = options.options.db_password
    add_linda_task_url = [u + options.options.add_linda for u in options.options.linda_url]
    linda_query_url = options.options.linda_query_url
    enable_redis = options.options.enable_redis
    redis_host = options.options.redis_host
    redis_port = options.options.redis_port
    max_retry = options.options.max_retry
    common_sleep_time = options.options.common_sleep_time
    fail_sleep_time = options.options.fail_sleep_time
    busy_max_send_num = options.options.busy_max_send_num
    idle_max_send_num = options.options.idle_max_send_num
    linda_query_interval = options.options.linda_query_interval

if __name__ == "__main__":
    conf = Conf()
    log.app_log.debug('server_port: %s' % conf.server_port)
    log.app_log.debug('service_interval: %s' % conf.service_interval)
    log.app_log.debug('check_new_since: %s' % conf.check_new_since)
    log.app_log.debug('enable_blacklist: %s' % conf.enable_blacklist)
    log.app_log.debug('db_host: %s' % conf.db_host)
    log.app_log.debug('db_port: %s' % conf.db_port)
    log.app_log.debug('db_name: %s' % conf.db_name)
    log.app_log.debug('db_user: %s' % conf.db_user)
    log.app_log.debug('db_password: %s' % conf.db_password)
    log.app_log.debug('add_linda_task_url: %s' % conf.add_linda_task_url)
    log.app_log.debug('linda_query_url: %s' % conf.linda_query_url)
    log.app_log.debug('enable_redis: %s' % conf.enable_redis)
    log.app_log.debug('redis_host: %s' % conf.redis_host)
    log.app_log.debug('redis_port: %s' % conf.redis_port)
    log.app_log.debug('max_retry: %s' % conf.max_retry)
    log.app_log.debug('common_sleep_time: %s' % conf.common_sleep_time)
    log.app_log.debug('fail_sleep_time: %s' % conf.fail_sleep_time)
    log.app_log.debug('busy_max_send_num: %s' % conf.busy_max_send_num)
    log.app_log.debug('idle_max_send_num: %s' % conf.idle_max_send_num)
    log.app_log.debug('linda_query_interval: %s' % conf.linda_query_interval)
    
