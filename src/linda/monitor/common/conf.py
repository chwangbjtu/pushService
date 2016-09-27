from tornado import options
from tornado import log

class Conf(object):
    options.define('db_host', type=str)
    options.define('db_port', type=int)
    options.define('db_name', type=str)
    options.define('db_user', type=str)
    options.define('db_password', type=str)
    options.define('redis_host', type=str)
    options.define('redis_port', type=int)
    options.define('redis_passwd', type=str)
    options.define('mail_host', type=str)
    options.define('mail_user', type=str)
    options.define('mail_passwd', type=str)
    options.define('mail_from', type=str)
    options.define('mail_to', type=list)
    options.define('mail_subject', type=str)

    options.parse_config_file('ds.conf')

    db_host = options.options.db_host
    db_port = options.options.db_port
    db_name = options.options.db_name
    db_user = options.options.db_user
    db_password = options.options.db_password
    redis_host = options.options.redis_host
    redis_port = options.options.redis_port
    redis_passwd = options.options.redis_passwd
    mail_host = options.options.mail_host
    mail_user = options.options.mail_user
    mail_passwd= options.options.mail_passwd
    mail_from = options.options.mail_from
    mail_to = options.options.mail_to
    mail_subject = options.options.mail_subject

if __name__ == "__main__":
    conf = Conf()
    log.app_log.debug('db_host: %s' % conf.db_host)
    log.app_log.debug('db_port: %s' % conf.db_port)
    log.app_log.debug('db_name: %s' % conf.db_name)
    log.app_log.debug('db_user: %s' % conf.db_user)
    log.app_log.debug('db_password: %s' % conf.db_password)
    log.app_log.debug('redis_host: %s' % conf.redis_host)
    log.app_log.debug('redis_port: %s' % conf.redis_port)
    log.app_log.debug('redis_passwd: %s' % conf.redis_passwd)
    log.app_log.debug('mail_host: %s' % conf.mail_host)
    log.app_log.debug('mail_user: %s' % conf.mail_user)
    log.app_log.debug('mail_passwd: %s' % conf.mail_passwd)
    log.app_log.debug('mail_from: %s' % conf.mail_from)
    log.app_log.debug('mail_to: %s' % conf.mail_to)
    log.app_log.debug('mail_subject: %s' % conf.mail_subject)
