#ifndef __MSG_CNT_MGR_H
#define __MSG_CNT_MGR_H
#include <iostream>
#include <map>
#include "kmutex.h"
#include "klock.h"

using namespace std;

class msg_cnt_struct
{
public:
    int _app_id;
    int _msg_id;
	int _resp_num;
	time_t _end_time;
};

class msg_cnt_mgr
{
public:
    ~msg_cnt_mgr(){}
    static msg_cnt_mgr * instance();
public:
    int push_msg(int appid,int msgid,time_t end_time);
    int erase_msg(int appid,int msgid);
    int erase_msg(int msgid);
	int incr(int appid,int msgid);
	int get_msg_list(map<long long,int>& msg_id_list);
    int aging(); 
private:
    msg_cnt_mgr();
    static msg_cnt_mgr * _inst;

    map<long long,msg_cnt_struct *> _msg;
 
    fsk::kshared_mutex  _mutex;   
};

#endif
