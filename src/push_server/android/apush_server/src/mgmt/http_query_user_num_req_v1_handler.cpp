#include <sstream>
#include <map>
#include <stdlib.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string>
#include "json/json.h"
#include "dbg.h"
#include "http_request.h"
#include "http_response.h"
#include "util.h"
#include "msg_mgr.h"
#include "msg_cnt_mgr.h"
#include "user_mgr.h"
#include "http_query_user_num_req_v1_handler.h"

using  fs::http_response;
using  fs::http_request;

int http_query_user_num_req_v1_handler::process(const fs::http_request& hr,unsigned int ip,string& resp)
{
    int res = 0;

    int user_num = 0;
    int conn_num = 0;
    int remain_num = 0;

	user_num = user_mgr::instance()->get_user_num();
    conn_num = user_mgr::instance()->get_conn_num();
    int max_user_num = 0;
    user_mgr::instance()->get_remain_num(max_user_num,remain_num);

    Json::Value item;
    stringstream ss;
    ss<<user_num;
    item["user_num"] = ss.str();
    ss.str("");
    ss<<conn_num;
    item["conn_num"] = ss.str();
    ss.str("");
    ss<<remain_num;
    item["remain_num"] = ss.str();

    map<int,int> app_user_num;
    user_mgr::instance()->get_app_user_num(app_user_num);
    map<int,string> app_list;
    util::instance()->get_app_list(app_list);

    Json::Value jmsg;
    map<int,string>::iterator iter = app_list.begin();
    for ( ;iter != app_list.end();iter++)
    {
        Json::Value titem;
        int num = 0;
        map<int,int>::iterator it = app_user_num.find(iter->first);
        if ( it != app_user_num.end())
        {
            num = it->second;
        }
        ss.str("");
        ss<<num;
        titem["app_name"] = iter->second;
        titem["num"] = ss.str();
        //titem[iter->second] = ss.str();
        jmsg.append(titem);
    }

    item["app"] = jmsg;
    
    string msg = item.toStyledString();
    

    http_response http_resp;
    http_resp._resp._content =msg;
    if(http_resp.pack(resp) < 0)
    { 
            return -1;
    }

	return 0;
}

