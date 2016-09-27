#ifndef __MSG_MGR_H
#define __MSG_MGR_H
#include <iostream>
#include <set>
#include <map>
#include "kmutex.h"
#include "klock.h"

using namespace std;

class msg_struct
{
public:
    string _msg;
    int     _msg_id;
    time_t _start_time;
    time_t _end_time;
    //bool   _global;
    //int    _appid;
    //set<int> _appids;
};

class msg_mgr
{
public:
    ~msg_mgr(){}
    static msg_mgr * instance();
public:
    //appid no use
    //int push_msg(int msgid, int appid,std::string&, time_t start_time, time_t end_time,bool global);
    int push_msg(int msgid, string& msg_type, string& msg, time_t end_time);
	int get_newest_msgid(int last_msgid, int appid);
    int get_msg(int msgid,string& msg);
    int get_msg(int msgid, msg_struct** msg);
	int erase_msg(int msgid);
    int aging(); 
private:
    msg_mgr();
    static msg_mgr * _inst;
    int _newest_msgid;
    //msg_id
    map<int,msg_struct *> _msg;
    fsk::kshared_mutex  _mutex;   
};

#endif
