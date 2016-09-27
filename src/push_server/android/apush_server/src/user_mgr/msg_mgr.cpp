#include "dbg.h"
#include "user_struct.h"
#include "msg_mgr.h"

msg_mgr::msg_mgr()
{
}

msg_mgr* msg_mgr::_inst = NULL;

msg_mgr* msg_mgr::instance()
{
    if ( _inst == NULL)
        _inst = new msg_mgr();
    return _inst;
}

//int msg_mgr::push_msg(int msgid,int appid,string& msg,time_t start_time,time_t end_time,bool global)
int msg_mgr::push_msg(int msgid, string& msg_type, string& msg, time_t end_time)
{
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    map<int,msg_struct *>::iterator iter = _msg.find(msgid);
    if ( iter == _msg.end())
    {
        msg_struct * pmsg = new msg_struct();
        pmsg->_msg_id = msgid;
        pmsg->_msg = msg;
        pmsg->_end_time = end_time;

        _msg[msgid] = pmsg;
        if(msg_type == "all"){
            _newest_msgid = msgid;
        } 
    }
    else
    {
        ;
    }
    return 0;
}

int msg_mgr::get_msg(int msgid,string& msg)
{
    int res = -1;
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    map<int,msg_struct *>::iterator iter = _msg.find(msgid);
    if ( iter != _msg.end())
    {
        msg = iter->second->_msg;
        res = 0;
    }

    return res;
}

int msg_mgr::get_msg(int msgid, msg_struct** msg)
{
    int res = -1;
    fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    map<int, msg_struct *>::iterator iter = _msg.find(msgid);
    if(iter != _msg.end())
    {
        *msg = iter->second;
        if (iter->second->_end_time >= time(NULL)) {
            res = 0;
        }
    }

    return res;
}

int msg_mgr::erase_msg(int msgid)
{
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    //map<int,msg_struct *>::iterator iter = _msg.begin();
    map<int,msg_struct *>::iterator iter = _msg.find(msgid);

    if ( iter != _msg.end())
    {
        delete iter->second;
        _msg.erase(iter++);
    }

    return 0;
}

int msg_mgr::get_newest_msgid(int last_msgid, int appid)
{   
    if(last_msgid != _newest_msgid) {
        return _newest_msgid;
    }
    return 0;
}

int msg_mgr::aging()
{
    fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
    time_t now = time(NULL);
    map<int,msg_struct *>::iterator iter = _msg.begin();
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
