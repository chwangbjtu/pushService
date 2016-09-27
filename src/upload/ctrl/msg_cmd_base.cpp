#include "msg_cmd_base.h"

msg_cmd_base::msg_cmd_base(int cnt,int msg_type,string taskid,string msg)
{
	_cnt = cnt;
	_msg_type = msg_type;
	_taskid = taskid;
	_msg = msg;

	if ( msg_type == send_upload_begin || msg_type == send_upload_finish)
	{
		_ip = tigress_conf::get_instance()->get_int_value("maze_ip");
		_port = tigress_conf::get_instance()->get_int_value("maze_port");
	}
	/*
	else if (msg_type == send_transcode)
	{
		_ip = tigress_conf::get_instance()->get_int_value("transcode_ip");
		_port = tigress_conf::get_instance()->get_int_value("transcode_port");
	}
	*/
	_last_send_time = 0;
		
}

msg_cmd_base::~msg_cmd_base()
{
}

int msg_cmd_base::get_cnt()
{
	return _cnt;
}

string msg_cmd_base::get_msg()
{
	return _msg;
}
	
void msg_cmd_base::set_msg(string msg)
{
	_msg = msg;
}
	
int msg_cmd_base::set_ip_port(unsigned int ip,unsigned short port)
{
	_ip=ip;
	_port=port;
	return 0;
}

unsigned int msg_cmd_base::get_ip()
{
	return _ip;
}
	
unsigned short msg_cmd_base::get_port()
{
	return _port;
}
	
int msg_cmd_base::add_cnt()
{
	_cnt++;
	_last_send_time = time(NULL);
	return 0;
}

string msg_cmd_base::get_taskid()
{
	return _taskid;
}
	
int msg_cmd_base::set_msg_type(int type)
{
	_msg_type = type; 
	return 0;
}

int msg_cmd_base::get_msg_type()
{
	return _msg_type;
}

time_t msg_cmd_base::get_last_time()
{
	return _last_send_time;
}

int msg_cmd_base::action() 
{
	return 0;
}


