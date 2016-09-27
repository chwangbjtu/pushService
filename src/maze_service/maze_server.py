#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import logging.handlers
import time
import os.path

import etc
import maze_thread
import video_manager
import http_server

def is_some_thread_dead(threads):
    for thrd in threads:
        if not thrd.is_alive():
            _critical = "thead with id = %s exited exceptionally" % (thrd.getName())
            logging.critical( _critical )
            return True
    
    return False

def mainloop(threads):
    logging.info("main-thread started!")
    while True:
        try:
            # do something like log statitics periodically
            time.sleep(5)
            if True == is_some_thread_dead(threads):
                return
        except KeyboardInterrupt:
            logging.warning( "maze server is interrupted by administrator")
            return
        except Exception, err:
            _warn = "Exception happened in main thread %s " % (err) 
            logging.warning("Exception happened in main thread %s", (err) )
        finally:
            pass
            
def init_db_dir():
    if os.path.exists(etc.DBPATH):
        pass
    else:
        logging.info("create db path: %s", etc.DBPATH)
        os.mkdir(etc.DBPATH)

def logger_init():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
                  etc.LOGPATH + "maze.log", mode='a', maxBytes=1024*1024*etc.MAX_LOGFILE_SIZE, backupCount=5)
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

def main():
    logger_init()
    init_db_dir()
    
    threads = []
    
    manager = video_manager.get_video_manager()
    manager.load_tasks() # load tasks from db
    manager.setName("video-manager-thread")
    manager.daemon  = True
    manager.start()
    threads.append(manager)
    
    server = http_server.HttpServer(etc.SERVICE_PORT)
    server.setName("http-server-thread")
    server.daemon  = True
    server.start()
    threads.append(server)
    
    maze_th_package = maze_thread.MazeThread("package")
    maze_th_package.setName("maze-thread-package")
    maze_th_package.daemon  = True
    maze_th_package.start()
    threads.append(maze_th_package)

    maze_th_distribute = maze_thread.MazeThread("distribute")
    maze_th_distribute.setName("maze-thread-distribute")
    maze_th_distribute.daemon  = True
    maze_th_distribute.start()
    threads.append(maze_th_distribute)
    
    time.sleep(1) # wait    
    return mainloop(threads)

if __name__ == "__main__":
    from daemonize import Daemonize
    daemon = Daemonize(app="mazed", pid=etc.pid, action=main)    
    daemon.start()
