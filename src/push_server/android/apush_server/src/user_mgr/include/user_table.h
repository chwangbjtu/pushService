#ifndef __USER_TABLE_H
#define __USER_TABLE_H

#include <string>
#include <map>
//#include "kmutex.h"

#include "user_struct.h"

using namespace std;

//const int MAX_CLIENT_NUM = 2000000;//200w
//const int MAX_CLIENT_NUM = 2000;//200w

class user_table
{
public:
	user_table();
	~user_table(){}
public:
    int start(int max_user_num);

    int push_gmsg(int app_type,int msg_id,int max_qps);

    //int push_msg(int uid,int msg_id,time_t pushtime);
    int push_msg(int uid,int msg_id,time_t now);

    //int get_uid(string token);
    //int init_uid(int uid);
    
    int erase_uid(int id,string& token,int& appid);

    int get_msgid(int uid,time_t now,map<int,int>& msg_list);

    int get_msgid(int uid,time_t now,int& msg_id);

    int erase_msg(int uid,int msgid,int& appid);
	
	int erase_msg(int msgid);

    //登陆时需要获取uid，如果时fudid重复了，就把uid带进来，reloign设置为true，让用户的引用计数加一
	//int get_uid(string token,int uid,bool relogin=false); 
	int get_uid();
    int login(int id,string& token,int app_id,unsigned int version,int area); 
    int relogin(int id);

    int get_user_info(int uid, user_struct& user);

    bool is_new_login(int id);

    int get_user_num(int& max_user_num,int& remain_num);
    //int get_app_user_num(map<int,int>& app_user_num);
private:

    //map<string,int> _task_id;//token to id
    //map<int,string> _rtask_id;//id to token
    map<int,int> _id_list;//id to id
    //map<int,int> _user_num;

    user_struct ** _pmsg_list;

    int _max_user_num;
    int _test;//test log
    int MAX_SEND_INTERVAL;

    //fsk::kunique_mutex _mutex;
};

#endif//__SESSION_MGR_H



