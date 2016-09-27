from tornado import options
from tornado import log
import sys
class Conf(object):
    options.define('server_port', type=int)

    options.parse_config_file('hs.conf')

    server_port = options.options.server_port

if __name__ == "__main__":
    conf = Conf()
    log.app_log.debug('server_port: %s' % conf.server_port)


