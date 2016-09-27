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
#include "http_pushgmsg_req_v2_handler.h"

using  fs::http_response;
using  fs::http_request;

int http_pushgmsg_req_v1_handler::process(const fs::http_request& hr,unsigned int ip,string& resp)
{
    http_response http_resp;

    int res = 0;
    //hr._req._content

    string info = hr._req._content;
	time_t now = time(NULL);

    Json::Reader reader(Json::Features::strictMode());
    Json::Value valuein;
    string smsg = "msg";
    string msg;
    if ( reader.parse(info,valuein))
    {
    }
    else
    {
        DBG_ERROR("parse json info error"); 
        return -1;
    }

    msg = valuein.toStyledString();
    

	string smsgid = "msgid";
    string msgid;
    if ( valuein.isMember(smsgid) && !valuein[smsgid].isNull()
            && valuein[smsgid].isString())
    {
        msgid = valuein[smsgid].asString();
    }
    else
    {
        DBG_ERROR("not find msgid");
        res = -1;
    }

    string spayload = "payload";
    string payload;
    if ( valuein.isMember(spayload) && !valuein[spayload].isNull()
            && valuein[spayload].isString())
    {
        payload = valuein[spayload].asString();
        DBG_INFO("%s",payload.data());
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
		//return -1;
	}

	//store msg
    string msg_type = "all";
    msg_mgr::instance()->push_msg(atoi(msgid.data()),msg_type,payload,expire_time);
    //0 is no use now,pace used for apptype
    user_mgr::instance()->push_gmsg(0,atoi(msgid.data()));


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

