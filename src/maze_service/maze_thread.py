#!/usr/bin/python
#-*- coding: utf-8 -*-
import time
import threading
import logging

import video_manager

class MazeThread(threading.Thread):
    def __init__(self, dispatch_type):
        threading.Thread.__init__(self)
        self._dispatch_type = dispatch_type
        self._manager   = video_manager.get_video_manager()
    
    def run(self):    
        """run the maze thread
        """
        _critical = "thread [%s] starts to run ... " % (self.getName())
        logging.critical( _critical )
        time.sleep(5)
        while True:
            try:
                task = self._manager.get_dispatch_task(self._dispatch_type)
                if not task and self._manager.redo_dispatch_tasks(self._dispatch_type) == 0:
                    logging.debug("does not get any task ... ")
                    time.sleep(5)
                    continue
                if task:
                    task.execute()
            except Exception, err:
                logging.warning("exception when running task's execute method %s", err)
                time.sleep(1)
            finally:
                pass
 
        logging.critical( "maze thread [%s] exits", self.getName() )    
 
