#include "dbg.h"
#include "tlogger.h"
#include "user_mgr.h"

user_mgr::user_mgr()
{
    _thread_num = 0;
}

user_mgr* user_mgr::_inst = NULL;

user_mgr* user_mgr::instance()
{
    if ( _inst == NULL)
        _inst = new user_mgr();
    return _inst;
}

int user_mgr::start(int thread_num,int max_user_num)
{
    _thread_num = thread_num;
    _ptable_list = new user_table * [thread_num];
    for ( int i=0;i<thread_num;i++)
    {
        _ptable_list[i] = new user_table();
        _ptable_list[i]->start(max_user_num/thread_num+1);
    }

    _remain_num = max_user_num;
    _max_user_num = max_user_num;

    return 0;
}

int user_mgr::push_gmsg(int app,int msgid)
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    int max_qps = configure::instance()->get_max_qps()/_thread_num;
    
    for ( int i=0;i<_thread_num;i++)
    {
        _ptable_list[i]->push_gmsg(app,msgid,max_qps);
    }

    return 0;
}

int user_mgr::push_msg(string token,int msgid,time_t now)
{
    int id = -1;
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    map<string,unsigned long long >::iterator iter = _task_id.find(token);
    if ( iter != _task_id.end())
    {
        int thread_id = (iter->second) >> 32;
        id = (iter->second) & 0x00000000ffffffff;//uid
        if (thread_id >= 0 && thread_id < _thread_num)    
        {
            _ptable_list[thread_id]->push_msg(id,msgid,now);
            id = 0;
        }
    }

    return id;
}

//user login used
int user_mgr::push_msg(string token,map<int,int>& msg_list,time_t now)
{
    int id = -1;
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    map<int,int>::iterator iter = msg_list.begin();
    for ( ; iter != msg_list.end();iter++)
    {
       id = push_msg(token,iter->first,now);
    }

    return id;
}

//int user_mgr::push_lmsg(list<string>& ltoken,int msgid,time_t pushtime)
int user_mgr::push_lmsg(list<string>& ltoken,int msgid,time_t now)
{
    if ( !ltoken.empty())
    {
        list<string>::iterator iter = ltoken.begin();
        for ( ;iter != ltoken.end();iter++)
        {
            push_msg(*iter,msgid,now);
        }
    }
    return 0;
}

int user_mgr::get_uid(int thread_index)
{

    int id = -1;
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    
    if ( _remain_num > _max_user_num/4 && thread_index >= 0&& thread_index < _thread_num)
    {
        id = _ptable_list[thread_index]->get_uid();
    }
    else
    {
        //DBG_ERROR("thread_id:%d,_remain_num:%d",thread_index,_remain_num);
        tlogger::instance()->mlog("ramin",fsk::level_t::warn_level(),_remain_num);
    }

    return id;
}

int user_mgr::login(int thread_index,int id,string& token,int app_id,unsigned int version,unsigned int area)
{
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    unsigned long long tid = thread_index;
    tid = tid << 32 | id;

    if ( thread_index >= 0 && thread_index < _thread_num)
    {
        if ( _ptable_list[thread_index]->is_new_login(id))
        {
            //cnt user_num
            map<int,int>::iterator iter = _user_num.find(app_id);
            if (iter != _user_num.end())
            {
                iter->second++;
            }
            else
            {
                _user_num[app_id] = 1;
            }

            //_task_id.insert(make_pair(token,tid));
            _task_id[token] = tid;

        }
        _ptable_list[thread_index]->login(id,token,app_id,version,area);
    }

    return 0;
}

int user_mgr::erase_uid(int thread_index,int id)
{
    int res = 0;
    if ( thread_index >= _thread_num || id < 0)
    {
        return -1;
    }
   
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    unsigned long long tid = thread_index;
    tid = tid << 32 | id;

    string token;
    int appid = -1;
    if ( thread_index >= 0 && thread_index < _thread_num)
    {
        _ptable_list[thread_index]->erase_uid(id,token,appid);
        //cnt user_num
        map<int,int>::iterator iter1 = _user_num.find(appid);
        if ( iter1 != _user_num.end())
        {
            if ( iter1->second >= 1)
            {
                iter1->second--;
            }
            else
            {
                ;
            }
        }
    }
    
    map<string,unsigned long long >::iterator iter = _task_id.find(token);
    if ( iter != _task_id.end())
    {
        _task_id.erase(iter);
    }

    return res;
}

int user_mgr::get_msgid(int thread_index,int uid,time_t now,map<int,int>& msg_list)
{
    int res = -1;
    if ( thread_index >= 0 && thread_index < _thread_num)
    {
        res = _ptable_list[thread_index]->get_msgid(uid,now,msg_list);
    }

    return res;
}

int user_mgr::get_msgid(int thread_index,int uid,time_t now,int& msg_id)
{
    int res = -1;
    if ( thread_index >= 0 && thread_index < _thread_num)
    {
        res = _ptable_list[thread_index]->get_msgid(uid,now,msg_id);
    }

    return res;
}

int user_mgr::erase_msg(int thread_index,int uid,int msgid,int& appid)
{
    int id = -1;
    if ( thread_index < _thread_num)
    {
        id = _ptable_list[thread_index]->erase_msg(uid,msgid,appid);
    }

    return id;
}

int user_mgr::erase_msg(int msgid)
{
    for ( int i=0;i < _thread_num;i++)
    {
        _ptable_list[i]->erase_msg(msgid);
    }

    return 0;
}

int user_mgr::get_user_info(string& token,user_struct& user)
{
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    int id = -1;
    map<string,unsigned long long >::iterator iter = _task_id.find(token);
    if ( iter != _task_id.end())
    {
        int thread_id = (iter->second) >> 32;
        id = (iter->second) & 0x00000000ffffffff;//uid
        if (thread_id >= 0 && thread_id < _thread_num)
        {
            //_ptable_list[thread_id]->push_msg(id,msgid,now);
            _ptable_list[thread_id]->get_user_info(id,user);
        }
    }

    return 0;
}

int  user_mgr::get_user_num()
{
    int num = 0;
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex); 
    num = _task_id.size();
    return num;
}

int user_mgr::get_conn_num()
{
    int num = 0;
    for ( int i=0;i<_thread_num;i++)
    {
        int max_user_num = 0;
        int remain_num = 0;
        _ptable_list[i]->get_user_num(max_user_num,remain_num);
        num += (max_user_num - remain_num);
    }

    return num;
}

int user_mgr::get_remain_num(int& gmax_usernum, int& gremain_num)
{
    for ( int i=0;i<_thread_num;i++)
    {
        int max_user_num = 0;
        int remain_num = 0;
        _ptable_list[i]->get_user_num(max_user_num,remain_num);
        gmax_usernum += max_user_num;
        gremain_num += remain_num;
    }

    _max_user_num = gmax_usernum;
    _remain_num = gremain_num;

    return 0;
}

int user_mgr::get_app_user_num(map<int,int>& app_user_num)
{
    app_user_num = _user_num;
    return 0;
}

