#!/usr/bin/python
# -*- coding:utf-8 -*- 
import ConfigParser
import utils

class ConfigMgr(object):
    def __init__(self):
        self.local_port = ""
        self.maze_ip = ""
        self.maze_port = ""

        self.file_dir = ""
        self.file_name = ""
        self.timeout_seconds = 30
        self.max_task_count = 1
        
        #about the log
        self.log_file_dir = None
        self.log_console_output = False
        self.log_level = "debug"

    def load_cfg(self,filepath):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read(filepath)
            self.local_port                  = get_section_keyvalue(cf,"server","local_port")
            self.maze_ip, self.maze_port     = get_section_keyvalue(cf,"server","maze_addr","maze_port")
            self.cloud_ip, self.cloud_port   = get_section_keyvalue(cf,"server","cloud_addr","cloud_port")
            self.file_dir, self.file_name    = get_section_keyvalue(cf,"workenv","file_dir","file_name")
            self.timeout_seconds             = get_section_keyvalue(cf,"workenv","timeout")
            self.max_task_count              = get_section_keyvalue(cf,"workenv","max_task_count")
            (self.log_file_dir, self.log_console_output, self.log_level) = \
                                get_section_keyvalue(cf,"log", "file_dir", "console_output", "level")
        except ConfigParser.NoOptionError:
            return False
        except ConfigParser.NoSectionError:
            return False
        except Exception,e:
            return False
        return True

    def check_env(self):
        port_list = (self.local_port,self.maze_port,)
        for port in port_list:
            if not utils.is_valid_port(port):
                return False
        #check directory
        if not utils.test_directory(self.file_dir):
            return False
        #check value
        try:
            self.timeout_seconds = float(self.timeout_seconds)
            self.max_task_count = int(self.max_task_count)
        except Exception:
            return False
        return True

cfg = None

def load_cfg(filepath):
    global cfg
    cfg = ConfigMgr()
    if not cfg.load_cfg(filepath):
        return False
    return cfg.check_env()

def get_maze_addr():
    return (cfg.maze_ip,cfg.maze_port)

def get_cloud_addr():
    return (cfg.cloud_ip,cfg.cloud_port)

def get_time_interval():
    return cfg.timeout_seconds

def get_max_task_count():
    return cfg.max_task_count

def get_local_addr():
    return cfg.local_port

def get_record_file():
    return "%s/%s" % (cfg.file_dir,cfg.file_name)

def get_log_cfg():
    return (cfg.log_file_dir,cfg.log_console_output,cfg.log_level)

def get_section_keyvalue(cf,section,*opt_list):
    result = []
    for key in opt_list:
        value = cf.get(section,key)
        result.append(value)
    if len(result) == 1:
        return result[0]
    return result

if __name__ == '__main__':
    load_cfg("etc/config.ini")
    print get_local_addr()
    print get_maze_addr()
    print get_cloud_addr()
    print get_record_file()
    print get_time_interval()
    print get_max_task_count()
    print get_log_cfg()
    raw_input()
    
        
