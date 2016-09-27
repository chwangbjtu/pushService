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
#include "http_pushmsg_req_v1_handler.h"

using  fs::http_response;
using  fs::http_request;

int http_pushmsg_req_v1_handler::process(const fs::http_request& hr,unsigned int ip,string& resp)
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

    //msg = valuein.toStyledString();
    

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

    string smsgtype = "msg_type";
    string msgtype;
    if ( valuein.isMember(smsgtype) && !valuein[smsgtype].isNull()
            && valuein[smsgtype].isString())
    {
        msgtype = valuein[smsgtype].asString();
    }
    else
    {
        DBG_ERROR("not find msg_type");
        res = -1;
    }

    string spayload = "msg_info";
    string payload;
    if ( valuein.isMember(spayload) && !valuein[spayload].isNull()
            && valuein[spayload].isString())
    {
        payload = valuein[spayload].asString();
    }
    else
    {
        DBG_ERROR("not find msg_info");
        res = -1;
    }

    int expire_time = now + configure::instance()->get_push_timeout();

    int imsgid = atoi(msgid.data());

	if ( msgid.size() == 0 || payload.size() == 0 || msgtype.size() == 0 || imsgid <= 0)
	{
        DBG_ERROR("%s,%s",msgid.data(),payload.data());
        res = -1;
		//return -1;
	}

    msg_cnt_mgr::instance()->push_msg(0,imsgid,expire_time);
    msg_mgr::instance()->push_msg(imsgid,msgtype,payload,expire_time);

    set<int> appids;
    if( msgtype == "test")
    {
        string sdevice_info = "device_info";
        string stoken = "token";
        if ( valuein.isMember(sdevice_info) && !valuein[sdevice_info].isNull())
        {
            if( valuein[sdevice_info].isMember(stoken) && !valuein[sdevice_info][stoken].isNull() && valuein[sdevice_info][stoken].isArray())
            {
                int size = valuein[sdevice_info][stoken].size();
                for ( int i=0;i<size;i++)
                {
                    if ( !valuein[sdevice_info][stoken][i].isNull() && valuein[sdevice_info][stoken][i].isString())
                    {
                        string token = valuein[sdevice_info][stoken][i].asString();

                        user_mgr::instance()->push_msg(token,imsgid,0);
                    }
                }
            }
        }
    }
    else if ( msgtype == "all")
    {
        //0 is no use now,used for apptype
        user_mgr::instance()->push_gmsg(0,atoi(msgid.data()));
    }
    else
    {
        res = -1;
        DBG_ERROR("msgtype error");
    }

	//store msg
    //msg_mgr::instance()->push_msg(atoi(msgid.data()),payload,expire_time);


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

