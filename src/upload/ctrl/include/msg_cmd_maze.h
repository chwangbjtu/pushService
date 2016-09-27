#ifndef __MSG_CMD_MAZE_H
#define __MSG_CMD_MAZE_H

#include <pthread.h>  
#include <iostream>
#include "msg_cmd_base.h"

using namespace std;

class msg_cmd_maze
{
public:
	msg_cmd_maze();
	~msg_cmd_maze(){};
	//virtual int action() {return 0;};
	void dispatch_first(msg_cmd_base * pmsg);
	void dispatch_second(msg_cmd_base * pmsg);
	msg_cmd_base * get_msg();
	bool first_send_over();
	bool second_send_over();
	void set_first_over();
	void set_second_over();
	bool has_first();
	bool has_second();
	void delete_all_cmd();
	void send_error(msg_cmd_base * pmsg);
protected:
	msg_cmd_base * _pfirst;//file uplaod begin msg
	msg_cmd_base * _psecond;//file upload over msg
	bool _first_send;
	bool _second_send;
	bool _first_send_over;
	bool _second_send_over;
	time_t _last_send_first;
	time_t _last_send_second;
	pthread_mutex_t _mutex ; 
};

#endif //__MSG_CMD_MAZE_H

