#ifndef __MSG_CMD_BASE_H
#define __MSG_CMD_BASE_H

#include <iostream>
#include <string>
#include "cmdq.h"
#include "ret_code.h"
#include "tigress_conf.h"

using namespace std;

class msg_cmd_base
{
public:
	
typedef enum {
	msg_type_sendmsg		= 0x0001
	
} msg_type_ft;

	msg_cmd_base(int cnt,int msg_type,string taskid,string msg);
	virtual ~msg_cmd_base();
	int get_cnt();
	string get_msg();
	void set_msg(string msg);
	int set_ip_port(unsigned int ip,unsigned short port);
	unsigned int get_ip();
	unsigned short get_port();
	int add_cnt();
	string get_taskid();
	int set_msg_type(int type);
	int get_msg_type();
	time_t get_last_time();
	int action() ;
protected:
	int 	_cnt;
	unsigned int _ip;
	unsigned short _port;
	int _msg_type;
	time_t _last_send_time;
	string _taskid;
	string _msg;
};

#endif //__MSG_CMD_BASE_H

