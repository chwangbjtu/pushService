#include <stdlib.h>
#include <sstream>
#include "json/json.h"
#include "http_request.h"
#include "util.h"
#include "task_report_push.h"
#include "dbg.h"
#include "msg_cnt_mgr.h"
#include "user_mgr.h"
#include "configure.h"
#include "msg_cmd_base.h"
#include "msg_manager.h"

using  fs::http_request;

task_report_push::task_report_push()
{
}

task_report_push::~task_report_push() 
{
}


int task_report_push::run(const time_t now)
{
    //int msg_cnt_mgr::get_msg_list(map<int,int>& msg_id_list)
    map<long long,int> msg_id_list;
    msg_cnt_mgr::instance()->get_msg_list(msg_id_list);
    if ( msg_id_list.size() == 0)
    {
        return 0;
    }

    //int total = user_mgr::instance()->get_user_num();
    int total = user_mgr::instance()->get_conn_num();

    map<int,int> app_user_num;
    user_mgr::instance()->get_app_user_num(app_user_num);
    int total_user_num = 0;
    map<int,int>::iterator it = app_user_num.begin();
    for(;it != app_user_num.end();it++)
    {
        total_user_num += it->second;
    }

    Json::Value jresp;
    
    //key is msgid,value is success num
    map<int,int> msg_num;
    Json::Value msg;
    map<long long,int>::iterator iter = msg_id_list.begin();
    for ( ;iter != msg_id_list.end();iter++)
    {
        int msg_id = -1;
        int appid = -1;
        parse_key(iter->first,appid,msg_id);
        
        if ( msg_num.find(msg_id) != msg_num.end())
        {
            msg_num[msg_id] += iter->second;
        }
        else
        {
            msg_num[msg_id] = iter->second;
        }
    }

    it = msg_num.begin();
    for(;it != msg_num.end();it++)
    {
        Json::Value titem;
        titem["type"] = "android";
        stringstream ss;
        ss<<it->first;
        titem["msgid"] = ss.str();
        ss.str("");
        ss<<it->second;
        titem["success"] = ss.str();
        ss.str("");
        ss<<total;
        titem["total_conn"] = ss.str();
        ss.str("");
        ss<<total_user_num;
        titem["user_num"] = ss.str();
        ss.str("");

        msg.append(titem);
    }

    jresp["result"] = msg;
    string sresp;
    //sresp = jresp.toStyledString();
    Json::FastWriter writer;  
    sresp = writer.write(jresp);

    string resp;
    pack_http_resp(sresp,resp);

    msg_cmd_base * pbase = new msg_cmd_base(resp);
    msg_manager::instance()->dispatch(pbase);

	return 0;
}


int task_report_push::pack_http_resp(string& body,string& resp)
{
    stringstream ss;
    ss<<body.size();
    string slen = ss.str();
    http_request http_req;
    http_req._req._method = "POST";
    http_req._req._path = "/v2/android/progress";
    http_req._req._version = "1.1";
    http_req._req._content = body;

    http_req._req._map_headers.insert(make_pair("Content-Type","application/x-www-form-urlencoded"));
    http_req._req._map_headers.insert(make_pair("Accept","*/*"));
    http_req._req._map_headers.insert(make_pair("Content-Length",slen));
    if (!configure::instance()->get_push_mgr_host().empty())
    {
        http_req._req._map_headers.insert(make_pair("Host", configure::instance()->get_push_mgr_host()));
    }
    /*stringstream ss1;
    string sip;
    util::instance()->ip2str(htonl(configure::instance()->get_trans_ip()),sip);
    ss1<<sip;
    ss1<<":";
    ss1<<configure::instance()->get_trans_port();
    string shost = ss1.str();
    http_req._req._map_headers.insert(make_pair("Host",shost));
    */

    /*
    if ( body.size() > 512)
    {
        DBG_ERROR("body is too long ,size:%d",body.size());
        return -1;
    }
    char cresp[1024]= {0};
    */

    string cresp;
    int tlen =  body.size() * 2;
    if ( tlen < 1024)
        tlen = 1024;

    char * pbuf = new char [tlen];

    int rlen = http_req.pack_post(pbuf,tlen-1);

    resp.assign(pbuf,rlen);
    delete pbuf;
    pbuf = NULL;
    //string tresp(cresp,rlen);
    //msg_cmd_base * pbase = new msg_cmd_maze(tresp);
    //msg_cmd_base * pbase = new msg_cmd_base(tresp);
    //msg_manager::instance()->dispatch(pbase);
    //cout<<"post req:"<<endl<<tresp<<endl;
    }

int task_report_push::parse_key(long long key,int& appid,int& msgid)
{
    appid = key >> 32;
    msgid = key & 0x00000000ffffffff;

    return 0;
}
