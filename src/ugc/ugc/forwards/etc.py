import ugc.settings as settings

maze_service_ip     = settings.MAZE_HOST
maze_service_port   = int(settings.MAZE_PORT)
maze_newtask_method = '/maze/addtask'

status_service = "http://%s:%d/maze/getstatus" % (maze_service_ip, maze_service_port)

