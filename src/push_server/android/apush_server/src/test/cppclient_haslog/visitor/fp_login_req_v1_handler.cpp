#include <stdlib.h>
#include <sstream>
#include <arpa/inet.h>
#include <string>
#include "json/json.h"
#include "dbg.h"
#include "proto_constant.h"
#include "proto_process.h"
#include "fp_login_req_v1_handler.h"

using namespace std;

int fp_login_req_v1_handler::process(string& req,unsigned int ip,int threadid,int& id,string& resp)
{
    const char* s = req.data();
     header_struct_t * p_req = (header_struct_t *)(req.data());
    if ( req.size() < p_req->size())
    {
        return -1;
    }
    int length = ntohl(p_req->_length);

    string sjson;
    if ( length < req.size())
    {
        sjson = req.substr(proto_header_len,length);
        string treq = req.substr(length);
        req = treq;
    }
    else if (length == req.size())
    {
        sjson = req.substr(proto_header_len,length);
        req.clear();
    }

    DBG_INFO("%s",sjson.data());

	return 0;
}

