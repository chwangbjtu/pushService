from tornado import options
from tornado import log

class Conf(object):
    options.define('server_port', type=int)    
    options.define('service_interval', type=int)    
    options.define('check_new_since', type=int)
    options.define('check_status_since', type=int)
    options.define('enable_blacklist',type=bool)
    options.define('db_host', type=str)
    options.define('db_port', type=int)
    options.define('db_name', type=str)
    options.define('db_user', type=str)
    options.define('db_password', type=str)
    options.define('maze_url', type=list)
    options.define('linda_url', type=list)
    options.define('flashget_url', type=list)
    options.define('add_task', type=str)
    options.define('add_linda', type=str)
    options.define('add_download', type=str)
    options.define('use_linda',type=bool)
    options.define('enable_redis',type=bool)
    options.define('redis_host', type=str)
    options.define('redis_port', type=int)
    options.define('kw_black_list', type=str)
    options.define('default_origin', type=str)
    options.define('default_uid', type=str)
    options.define('customer_uid', type=str)
    options.define('default_priority', type=str)
    options.define('max_retry', type=int)
    options.define('common_sleep_time', type=int)
    options.define('fail_sleep_time', type=int)
    options.define('block_sleep_time', type=int)

    options.define('maze_url_addr', type=dict)
    options.define('flashget_url_addr', type=dict)
    options.define('enable_addr',type=bool)
    options.parse_config_file('ds.conf')

    server_port = options.options.server_port
    service_interval = options.options.service_interval
    check_new_since = options.options.check_new_since
    check_status_since = options.options.check_status_since
    enable_blacklist = options.options.enable_blacklist
    db_host = options.options.db_host
    db_port = options.options.db_port
    db_name = options.options.db_name
    db_user = options.options.db_user
    db_password = options.options.db_password
    add_maze_task_url = [u + options.options.add_task for u in options.options.maze_url]
    add_linda_task_url = [u + options.options.add_linda for u in options.options.linda_url]
    add_flashget_task_url = [u + options.options.add_download for u in options.options.flashget_url]
    use_linda = options.options.use_linda
    enable_redis = options.options.enable_redis
    redis_host = options.options.redis_host
    redis_port = options.options.redis_port
    kw_black_list = options.options.kw_black_list
    default_origin = options.options.default_origin
    default_uid = options.options.default_uid
    customer_uid = options.options.customer_uid
    default_priority = options.options.default_priority
    max_retry = options.options.max_retry
    common_sleep_time = options.options.common_sleep_time
    fail_sleep_time = options.options.fail_sleep_time
    block_sleep_time = options.options.block_sleep_time

    add_maze_task_url_addr= {}
    for k in options.options.maze_url_addr:
        add_maze_task_url_addr[k] = [u + options.options.add_task for u in options.options.maze_url_addr[k]]

    add_flashget_task_url_addr= {}
    for k in options.options.flashget_url_addr:
        add_flashget_task_url_addr[k]= [u + options.options.add_download for u in options.options.flashget_url_addr[k]]
    
    enable_addr=options.options.enable_addr
if __name__ == "__main__":
    conf = Conf()
    print conf.add_flashget_task_url
    print conf.add_flashget_task_url_addr
    print conf.add_maze_task_url_addr
    print conf.add_maze_task_url
    log.app_log.debug('server_port: %s' % conf.server_port)
    log.app_log.debug('service_interval: %s' % conf.service_interval)
    log.app_log.debug('check_new_since: %s' % conf.check_new_since)
    log.app_log.debug('check_status_since: %s' % conf.check_status_since)
    log.app_log.debug('enable_blacklist: %s' % conf.enable_blacklist)
    log.app_log.debug('db_host: %s' % conf.db_host)
    log.app_log.debug('db_port: %s' % conf.db_port)
    log.app_log.debug('db_name: %s' % conf.db_name)
    log.app_log.debug('db_user: %s' % conf.db_user)
    log.app_log.debug('db_password: %s' % conf.db_password)
    log.app_log.debug('add_maze_task_url: %s' % conf.add_maze_task_url)
    log.app_log.debug('add_linda_task_url: %s' % conf.add_linda_task_url)
    log.app_log.debug('add_flashget_task_url: %s' % conf.add_flashget_task_url)
    log.app_log.debug('use_linda: %s' % conf.use_linda)
    log.app_log.debug('enable_redis: %s' % conf.enable_redis)
    log.app_log.debug('redis_host: %s' % conf.redis_host)
    log.app_log.debug('redis_port: %s' % conf.redis_port)
    log.app_log.debug('kw_black_list: %s' % conf.kw_black_list)
    log.app_log.debug('default_origin: %s' % conf.default_origin)
    log.app_log.debug('default_uid: %s' % conf.default_uid)
    log.app_log.debug('customer_uid: %s' % conf.customer_uid)
    log.app_log.debug('default_priority: %s' % conf.default_priority)
    log.app_log.debug('max_retry: %s' % conf.max_retry)
    log.app_log.debug('common_sleep_time: %s' % conf.common_sleep_time)
    log.app_log.debug('fail_sleep_time: %s' % conf.fail_sleep_time)
    log.app_log.debug('block_sleep_time: %s' % conf.block_sleep_time)
