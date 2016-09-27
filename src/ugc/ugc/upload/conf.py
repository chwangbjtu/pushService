#!/usr/bin/python
# -*- coding:utf-8 -*-
import ugc.settings as settings
MAZE_APPLY_TASK_URL  = "http://%s:%s/maze/addtask"   % (settings.MAZE_HOST, settings.MAZE_PORT)
MAZE_REPORT_TASK_URL = "http://%s:%s/maze/addstatus" % (settings.MAZE_HOST, settings.MAZE_PORT)
