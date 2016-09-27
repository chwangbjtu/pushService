#include "dbg.h"
#include "configure.h"
#include "tlogger.h"
#include "user_table.h"

user_table::user_table()
{
    _max_user_num = 0;
    _test = configure::instance()->get_test();
    MAX_SEND_INTERVAL = configure::instance()->get_repush_interval();
}

int user_table::start(int num)
{
    _max_user_num = num;
    _pmsg_list = new user_struct * [num];
    for(int i=0;i<num;i++)
    {
        _id_list.insert(make_pair(i,i));
        _pmsg_list[i] = new user_struct();
    }
}

//每秒推送消息给固定用户(qps)，超过qps后发送时间延后1秒
int user_table::push_gmsg(int app,int msgid,int qps)
{
    time_t now = time(NULL) - MAX_SEND_INTERVAL;
    int cnt = 0;
    for(int i=0;i<_max_user_num;i++)
    {
        //已登陆用户
        //if ( _pmsg_list[i]->_flag > 0 && app == _pmsg_list[i]->_app_type)
        if ( _pmsg_list[i]->_flag > 0)
        {
            int j = 0;
            for ( ;j<MAX_MSG_NUM;j++)
            {
                if ( _pmsg_list[i]->_last_send_time[j] == -1)
                {
                    _pmsg_list[i]->_last_send_time[j] = now;
                    _pmsg_list[i]->_msg_list[j] = msgid;
                    cnt++;
                    break;
                }
            }
            //msgid is full
            if ( j == MAX_MSG_NUM)
            {
                _pmsg_list[i]->_last_send_time[0] = now;
                _pmsg_list[i]->_msg_list[0] = msgid;
                cnt++;
            }
        }
        if ( cnt >= qps)
        {
            cnt = 0;
            now += 1;
        }
    }

    return 0;
}

int user_table::push_msg(int uid,int msg_id,time_t now)
{
    if ( uid < 0 || uid >= _max_user_num || msg_id < 0)
    {
        return -1;
    }

    if ( _pmsg_list[uid]->_flag > 0)
    {
        int i = 0;
        for(;i<MAX_MSG_NUM;i++)
        {
            //_pmsg_list[uid]->_last_send_time[i]
            if ( _pmsg_list[uid]->_last_send_time[i] == -1)
            {
                _pmsg_list[uid]->_last_send_time[i] = now;
                _pmsg_list[uid]->_msg_list[i] = msg_id;
                break;
            }
        }
        //msgid is full
        if ( i == MAX_MSG_NUM)
        {
            _pmsg_list[uid]->_last_send_time[0] = now;
            _pmsg_list[uid]->_msg_list[0] = msg_id;
        }
    }
    
    return 0;
}

bool user_table::is_new_login(int uid)
{
    if ( uid < 0 || uid >= _max_user_num)
    {
        return false;
    }
    return _pmsg_list[uid]->_new_login;
}

int user_table::login(int uid,string& token,int app_id,unsigned int version,int area)
{
    if ( uid < 0 || uid >= _max_user_num)
    {
        return -1;
    }

    _pmsg_list[uid]->_token = token;
    _pmsg_list[uid]->_app_type = app_id;
    _pmsg_list[uid]->_version = version;
    _pmsg_list[uid]->_area = area;
    _pmsg_list[uid]->_new_login = false;

    tlogger::instance()->log("login",fsk::level_t::info_level(),token,area,version,1);

    return 0;
}

int user_table::get_user_info(int uid,user_struct& user)
{
    if ( uid < 0 || uid >= _max_user_num)
    {
        return -1;
    }

    user._token = _pmsg_list[uid]->_token;
    user._app_type = _pmsg_list[uid]->_app_type;
    user._version = _pmsg_list[uid]->_version;
    user._area = _pmsg_list[uid]->_area;
    user._new_login = _pmsg_list[uid]->_new_login;

    return 0;
}

int user_table::get_uid()
{
    int id = -1;
    if ( _id_list.size() > 0)
    {
        map<int,int>::iterator it = _id_list.begin();
        id = it->first;
        _id_list.erase(it);
        if ( id >= 0 && id < _max_user_num)
        {
            _pmsg_list[id]->_flag = 1;
        }
    }
    else
    {
        //DBG_ERROR("id_list have no id");
        tlogger::instance()->mlog("uid_not_enough",fsk::level_t::warn_level(),0);
    }

    return id;
}

int user_table::erase_uid(int id,string& token,int& appid)
{
    if ( id < 0 || id >= _max_user_num)
    {
        return -1;
    }

    _pmsg_list[id]->_flag = 0;

    for(int i=0;i<MAX_MSG_NUM;i++)
    {
        _pmsg_list[id]->_last_send_time[i] = no_msg;
    }
    _id_list.insert(make_pair(id,id));
    token = _pmsg_list[id]->_token;
    appid = _pmsg_list[id]->_app_type;
    _pmsg_list[id]->_new_login = true;
    
    return 0;
}

int user_table::get_msgid(int uid,time_t now,map<int,int>& msg_list)
{
    int msgid = -1;
    if ( uid < 0 || uid >= _max_user_num)
    {
        return msgid;
    }
   
    if ( _pmsg_list[uid]->_flag > 0)
    {
        for(int i=0;i<MAX_MSG_NUM;i++)
        {
            if ( now >= _pmsg_list[uid]->_last_send_time[i] + MAX_SEND_INTERVAL && _pmsg_list[uid]->_last_send_time[i] != -1)
            {
                _pmsg_list[uid]->_last_send_time[i] = now;
                msgid = _pmsg_list[uid]->_msg_list[i];
                msg_list.insert(make_pair(msgid,msgid));
                tlogger::instance()->log("push",fsk::level_t::debug_level(),_pmsg_list[uid]->_token,msgid,0);
                //break;
            }
        }
    }
    return msgid;
}

int user_table::get_msgid(int uid,time_t now,int& msg_id)
{
    int res = -1;
    if ( uid < 0 || uid >= _max_user_num)
    {
        return res;
    }

    if ( _pmsg_list[uid]->_flag > 0)
    {
        for(int i=0;i<MAX_MSG_NUM;i++)
        {
            if ( now >= _pmsg_list[uid]->_last_send_time[i] + MAX_SEND_INTERVAL && _pmsg_list[uid]->_last_send_time[i] != -1)
            {
                _pmsg_list[uid]->_last_send_time[i] = now;
                msg_id = _pmsg_list[uid]->_msg_list[i];
                res = 0;
                tlogger::instance()->log("push",fsk::level_t::debug_level(),_pmsg_list[uid]->_token,msg_id,0);
                break;
            }
        }
    }
    return res;
}

int user_table::erase_msg(int uid,int msgid,int& appid)
{
    if ( uid < 0 || uid >= _max_user_num)
    {
        return -1;
    }

    if ( _pmsg_list[uid]->_flag > 0)
    {
        for(int i=0;i<MAX_MSG_NUM;i++)
        {
            if ( _pmsg_list[uid]->_msg_list[i] == msgid)
            {
                _pmsg_list[uid]->_last_send_time[i] = no_msg;
                _pmsg_list[uid]->_msg_list[i] = no_msg;
                appid = _pmsg_list[uid]->_app_type;
                break;
            }
        }
        //tlogger::instance()->log(_pmsg_list[uid]->_token,_pmsg_list[uid]->_area,
        //     _pmsg_list[uid]->_version,0,msgid,1);
        tlogger::instance()->log("push",fsk::level_t::debug_level(),_pmsg_list[uid]->_token,msgid,1);
        
    }

    return 0;
}

int user_table::erase_msg(int msgid)
{
	for( int i=0;i<_max_user_num;i++)
	{
		if ( _pmsg_list[i]->_flag <= 0)
			continue;
    	for(int j=0;j<MAX_MSG_NUM;j++)
    	{
        	if ( _pmsg_list[i]->_msg_list[j] == msgid)
        	{
           		_pmsg_list[i]->_last_send_time[j] = no_msg;
            	_pmsg_list[i]->_msg_list[j] = no_msg;
            	break;
       		}
    	}
	}

    return 0;
}

int user_table::get_user_num(int& max_user_num,int& remain_num)
{
    max_user_num = _max_user_num;
    remain_num = _id_list.size();
    return 0;
}

