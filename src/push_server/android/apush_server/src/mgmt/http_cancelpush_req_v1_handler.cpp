#include <map>
#include <stdlib.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string>
#include "json/json.h"
#include "dbg.h"
#include "http_request.h"
#include "http_response.h"
#include "msg_mgr.h"
#include "msg_cnt_mgr.h"
#include "user_mgr.h"
#include "http_cancelpush_req_v1_handler.h"

using  fs::http_response;
using  fs::http_request;

int http_cancelpush_req_v1_handler::process(const fs::http_request& hr,unsigned int ip,string& resp)
{
    int res = 0;

    const string smsgid = "msgid";
    multimap<string,string>::const_iterator iter;
    iter = hr._req._map_params.find(smsgid);
    string msgid;
    if ( iter != hr._req._map_params.end())
    {
        if ( !iter->second.empty())
        {
            msgid = iter->second;
        }
    }
    else
    {
        return -1;
    }

    int imsgid = -1;
    imsgid = atoi(msgid.data());

    http_response http_resp;
    http_resp._resp._content ="{\"retcode\":\"200\",\"retmsg\":\"ok\"}";

	if ( imsgid >= 0)
	{
		msg_mgr::instance()->erase_msg(imsgid);
        msg_cnt_mgr::instance()->erase_msg(imsgid);
	    //user_mgr::instance()->erase_msg(imsgid,imsg_id);
	}
    else
    {
        http_resp._resp._content ="{\"retcode\":\"404\",\"retmsg\":\"para error\"}";
    }


    if(http_resp.pack(resp) < 0)
    { 
            return -1;
    }

	return 0;
}

