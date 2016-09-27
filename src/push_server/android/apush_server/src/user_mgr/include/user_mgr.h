#ifndef __USER_MGR_H
#define __USER_MGR_H

#include <string>
#include <map>
#include <set>
#include <list>
#include "kmutex.h"

#include "user_struct.h"
#include "user_table.h"

using namespace std;

//const int MAX_CLIENT_NUM = 2000000;//200w
//

class user_mgr
{
public:
	~user_mgr(){}
	static user_mgr* instance();
public:
    int start(int thread_num,int max_user_num);

    int push_gmsg(int appid,int msg_id);

    //int push_msg(string token,int msgid,time_t pushtime);
    int push_msg(string token,int msgid,time_t now);

    //int push_lmsg(list<string>& ltoken,int msgid,time_t pushtime);
    int push_lmsg(list<string>& ltoken,int msgid,time_t now);

    int push_msg(string token,map<int,int>& msg_list,time_t now);

    int get_uid(int thread_index,string& token);

    int get_uid(int thread_index);

    int login(int thread_index,int id,string& token,int app_id,unsigned int version,unsigned int loc);

    int erase_uid(int thread_index,int id);

	int get_msgid(int thread_index,int uid,time_t now,map<int,int>& msg_list);

    int get_msgid(int thread_index,int uid,time_t now,int& msg_id);

    int erase_msg(int thread_index,int uid,int msgid,int& appid); 

	int erase_msg(int msgid);

    int get_user_info(std::string& token, user_struct& user);

    int get_user_num();

    int get_conn_num();

    int get_remain_num(int& gmax_usernum, int& gremain_num);

    int get_app_user_num(map<int,int>& app_user_num);

private:
	user_mgr();
	static user_mgr* _inst;

    int _thread_num;
    user_table ** _ptable_list;

    //user_mgr 中存放_rtask_id,就是为了个性化推送时能通过token找到threadid和id
    //map<string,unsigned long long> _task_id;//token to id
    map<string,unsigned long long > _task_id;//token to id,id is thread_index_index
    //map<unsigned long long,string> _rtask_id;//id to token
    //map<int,int> _id_list;//id to id
    map<int,int> _user_num;//;appid,num
    int _remain_num;
    int _max_user_num;

    fsk::kshared_mutex  _mutex;
};

#endif//__USER_MGR_H



