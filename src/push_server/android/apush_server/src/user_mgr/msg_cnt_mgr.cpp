#include <sstream>
#include "dbg.h"
#include "msg_cnt_mgr.h"

using namespace std;

msg_cnt_mgr::msg_cnt_mgr()
{
}

msg_cnt_mgr* msg_cnt_mgr::_inst = NULL;

msg_cnt_mgr* msg_cnt_mgr::instance()
{
    if ( _inst == NULL)
        _inst = new msg_cnt_mgr();
    return _inst;
}

int msg_cnt_mgr::push_msg(int appid,int msgid,time_t end_time)
{
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    long long nmsgid = appid;
    nmsgid = nmsgid<<32|msgid;
    //DBG_INFO("%llu,%d,%d",nmsgid,appid,msgid);
    map<long long,msg_cnt_struct *>::iterator iter = _msg.find(nmsgid);
    if ( iter == _msg.end())
    {
        msg_cnt_struct * pmsg = new msg_cnt_struct();
        pmsg->_app_id = appid;
        pmsg->_msg_id = msgid;
        pmsg->_resp_num = 0;
        pmsg->_end_time = end_time;

        _msg[nmsgid] = pmsg;
    }
    
    return 0;
}

int msg_cnt_mgr::erase_msg(int msgid)
{
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    map<long long,msg_cnt_struct *>::iterator iter = _msg.begin();
    for ( ;iter!= _msg.end();)
    {
        if ( iter->second->_msg_id == msgid)
        {
            delete iter->second;
            _msg.erase(iter++);
        }
        else
            iter++;
    }

    return 0;
}

int msg_cnt_mgr::get_msg_list(map<long long,int>& msg_id_list)
{
	int res = 0;
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    map<long long,msg_cnt_struct *>::iterator iter = _msg.begin();
    for ( ;iter != _msg.end();iter++)
    {
		msg_id_list.insert(make_pair(iter->first,iter->second->_resp_num));
    }

    return res;
}

int msg_cnt_mgr::incr(int appid,int msgid)
{
    int res = 0;
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    long long nmsgid = appid;
    nmsgid = nmsgid<<32 | msgid;
    map<long long,msg_cnt_struct *>::iterator iter = _msg.find(nmsgid);
    if ( iter != _msg.end())
    {
        iter->second->_resp_num++;
    }
    else
    {
        /*
        msg_cnt_struct * pmsg = new msg_cnt_struct();
        pmsg->_app_id = appid;
        pmsg->_msg_id = msgid;
        pmsg->_resp_num = 1;
        pmsg->_end_time = time(NULL) + 24*3600;

        _msg[nmsgid] = pmsg;
        */
    }

    return res;
}

int msg_cnt_mgr::aging()
{
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    time_t now = time(NULL);
    map<long long,msg_cnt_struct *>::iterator iter = _msg.begin();
    while(iter != _msg.end())
    {
        if ( iter->second->_end_time < now)
        {
            delete iter->second;
            _msg.erase(iter++);
        }
        else
        {
            iter++;
        }
    }

    return 0;
}
