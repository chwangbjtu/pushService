#ifndef __USER_STRUCT_H
#define __USER_STRUCT_H

#include "configure.h"
#include <iostream>

using namespace std;

const int MAX_MSG_NUM = 8;
//const int MAX_MSG_NUM = configure::instance()->get_max_msg_num();

//const int MAX_SEND_INTERVAL = 10;
//const int MAX_SEND_INTERVAL = configure::instance()->get_repush_interval();

typedef enum
{
    no_msg = -1,
    has_msg = 0,
    sending_msg = 1,
    sended_msg = 2
}msg_state_t;

class user_struct
{
public:
    user_struct()
    {
        for(int i=0;i<MAX_MSG_NUM;i++)
        {
            _msg_list[i] = -1;
            _last_send_time[i] = -1;
            //_pu_id[i] = -1;
        }
        _flag = 0;
        _new_login = true;
    }

public:
    int _msg_list[MAX_MSG_NUM];
    int _last_send_time[MAX_MSG_NUM];
    //int _pu_id[MAX_MSG_NUM];
    int _flag;//该结构中是否保存有用户数据
    string _token;
    unsigned int _version;
    int _app_type;
    unsigned short _area;
    bool _new_login;
    unsigned short _isp;
};

#endif//__USER_STRUCT_H
