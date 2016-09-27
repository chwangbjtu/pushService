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
#include "http_pushtmsg_req_v2_handler.h"

using  fs::http_response;
using  fs::http_request;

int http_pushtmsg_req_v2_handler::process(const fs::http_request& hr,unsigned int ip,string& resp)
{
    http_response http_resp;

    int res = 0;
    //hr._req._content

    string info = hr._req._content;
    time_t now = time(NULL);

    Json::Reader reader(Json::Features::strictMode());
    Json::Value valuein;
    string smsg = "msg";
    if ( reader.parse(info,valuein))
    {
    }
    else
    {
        DBG_ERROR("parse json info error"); 
        return -1;
    }

    string smsgid = "msgid";
    string msgid;
    if ( valuein.isMember(smsgid) && !valuein[smsgid].isNull()
            && valuein[smsgid].isString())
    {
        msgid = valuein[smsgid].asString();
    }
    else
    {
        DBG_ERROR("not find msg_id");
        res = -1;
    }

    string spaylaod = "payload";
    string payload;
    if ( valuein.isMember(spaylaod) && !valuein[spaylaod].isNull()
            && valuein[spaylaod].isString())
    {
        payload = valuein[spaylaod].asString();
    }
    else
    {
        DBG_ERROR("not find payload");
        res = -1;
    }

    int expire_time = now + 3600 * 24;


    if ( msgid.size() == 0 || payload.size() == 0)
    {
        DBG_ERROR("%s,%s",msgid.data(),payload.data());
        res = -1;
    }

    DBG_INFO("%s,%d,%d",msgid.data(),payload.size(),expire_time);
    string msg_type = "test";
    msg_mgr::instance()->push_msg(atoi(msgid.data()),msg_type,payload,expire_time);

    string stoken = "token";
    string sid = "id";
    string sapp_name = "app_name";

    //store msg
    if ( valuein.isMember(stoken) && !valuein[stoken].isNull())
    {
        //Json::Value avalue = value[sdevice_token];
        int size = valuein[stoken].size();
        for ( int i=0;i<size;i++)
        {
            //if (  value[sdevice_token][i].isMember(sapp_name) && ! value[sdevice_token][i][sapp_name].isNull()
            //    &&  value[sdevice_token][i][sapp_name].isString())
            if (  valuein[stoken][i].isMember(sid) && ! valuein[stoken][i][sid].isNull()
                &&  valuein[stoken][i][sid].isString())
            {
                string token = valuein[stoken][i][sid].asString();
                //string app_name = value[sdevice_token][i][sapp_name].asString();
                //int app_id = util::instance()->get_app_id(app_name);
                //if ( app_id != -1)
                {
                    //msg_cnt_mgr::instance()->push_msg(app_id,atoi(pu_id.data()),atoi(msgid.data()),expire_time);
                    DBG_INFO("");
                    user_mgr::instance()->push_msg(token,atoi(msgid.data()),0);
                }
            }
        }
    }
    else
    {
        res = -1;
    }

    if ( res == 0) 
    {
        http_resp._resp._content ="{\"retcode\":\"200\",\"retmsg\":\"ok\"}";
    }
    else
    {
        http_resp._resp._content ="{\"retcode\":\"404\",\"retmsg\":\"\"}";
    }

    if(http_resp.pack(resp) < 0)
    { 
        DBG_ERROR("pack error");
        return -1;
    }

    return 0;
}

