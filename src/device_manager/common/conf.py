from tornado import options
from tornado import log

class Conf(object):
    options.define('mg_host', type=str)
    options.define('mg_name', type=str)
    options.define('mg_user', type=str)
    options.define('mg_password', type=str)
    options.define('mg_retry_time', type=int)

    options.parse_config_file('work.conf')

    mg_host = options.options.mg_host
    mg_name = options.options.mg_name
    mg_user = options.options.mg_user
    mg_password = options.options.mg_password
    mg_retry_time = options.options.mg_retry_time

if __name__ == "__main__":
    conf = Conf()
