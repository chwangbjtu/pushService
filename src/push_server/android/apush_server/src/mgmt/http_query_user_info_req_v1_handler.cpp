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
#include "http_query_user_info_req_v1_handler.h"

using  fs::http_response;
using  fs::http_request;

int http_query_user_info_req_v1_handler::process(const fs::http_request& hr,unsigned int ip,string& resp)
{
    int res = 0;

    const string stoken = "token";
    multimap<string,string>::const_iterator iter;
    iter = hr._req._map_params.find(stoken);
    string token;
    if ( iter != hr._req._map_params.end())
    {
        if ( !iter->second.empty())
        {
            token = iter->second;
        }
    }
    else
    {
        return -1;
    }

    user_struct user;
    res = user_mgr::instance()->get_user_info(token,user);
    if ( user._token.size() > 0)
    {
        resp = util::instance()->get_http_200_resp();
    }
    else
    {
        resp = util::instance()->get_http_404_resp();
    }

	return 0;
}

