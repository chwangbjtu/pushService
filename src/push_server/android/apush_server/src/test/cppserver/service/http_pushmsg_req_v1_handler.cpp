#include <map>
#include <stdlib.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string>
#include "http_request.h"
#include "http_response.h"
#include "http_pushmsg_req_v1_handler.h"

using  fs::http_response;
using  fs::http_request;

int http_pushmsg_req_v1_handler::process(const fs::http_request& hr,unsigned int ip,string& resp)
{
    http_response http_resp;
    int res = 0;

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
        return -1;
    }

	return 0;
}

