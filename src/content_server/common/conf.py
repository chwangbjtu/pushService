from tornado import options
from tornado import log

class Conf(object):
    options.define('server_port', type=int)
    options.define('mg_host', type=str)
    options.define('mg_name', type=str)
    options.define('mg_user', type=str)
    options.define('mg_password', type=str)
    options.define('mg_retry_time', type=int)
    options.define('process_num', type=int)
    options.define('idle_connection_timeout', type=int)

    options.parse_config_file('work.conf')

    server_port = options.options.server_port
    mg_host = options.options.mg_host
    mg_name = options.options.mg_name
    mg_user = options.options.mg_user
    mg_password = options.options.mg_password
    mg_retry_time = options.options.mg_retry_time
    process_num = options.options.process_num
    idle_connection_timeout = options.options.idle_connection_timeout
if __name__ == "__main__":
    conf = Conf()
    print conf.idle_connection_timeout
