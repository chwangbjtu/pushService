from tornado import options
from tornado import log

class Conf(object):
    options.define('server_port', type=int)    
    options.define('maze_url', type=list)
    options.define('add_task', type=str)
    options.define('enable_redis',type=bool)
    options.define('redis_host', type=str)
    options.define('redis_port', type=int)
    options.define('default_origin', type=str)
    options.define('default_uid', type=str)
    options.define('default_priority', type=str)
    options.define('max_retry', type=int)
    options.define('common_sleep_time', type=int)
    options.define('fail_sleep_time', type=int)

    options.parse_config_file('vps.conf')

    server_port = options.options.server_port
    add_maze_task_url = [u + options.options.add_task for u in options.options.maze_url]
    enable_redis = options.options.enable_redis
    redis_host = options.options.redis_host
    redis_port = options.options.redis_port
    default_origin = options.options.default_origin
    default_uid = options.options.default_uid
    default_priority = options.options.default_priority
    max_retry = options.options.max_retry
    common_sleep_time = options.options.common_sleep_time
    fail_sleep_time = options.options.fail_sleep_time

if __name__ == "__main__":
    conf = Conf()
    log.app_log.debug('server_port: %s' % conf.server_port)
    log.app_log.debug('add_maze_task_url: %s' % conf.add_maze_task_url)
    log.app_log.debug('enable_redis: %s' % conf.enable_redis)
    log.app_log.debug('redis_host: %s' % conf.redis_host)
    log.app_log.debug('redis_port: %s' % conf.redis_port)
    log.app_log.debug('default_origin: %s' % conf.default_origin)
    log.app_log.debug('default_uid: %s' % conf.default_uid)
    log.app_log.debug('default_priority: %s' % conf.default_priority)
    log.app_log.debug('max_retry: %s' % conf.max_retry)
    log.app_log.debug('common_sleep_time: %s' % conf.common_sleep_time)
    log.app_log.debug('fail_sleep_time: %s' % conf.fail_sleep_time)
