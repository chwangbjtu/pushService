#include <arpa/inet.h>
#include <string>
#include "json/json.h"
#include "dbg.h"
#include "proto_constant.h"
#include "proto_process.h"
#include "fp_htbt_req_v1_handler.h"
#include "tlogger.h"

int fp_htbt_req_v1_handler::process(string& req,unsigned int ip,int threadid,int& id,string& token,string& resp)
{
    const char* s = req.data(); 
     header_struct_t * p_req = (header_struct_t *)(req.data());
    if ( req.size() < p_req->size())
    {
        tlogger::instance()->log("htbtp",fsk::level_t::debug_level(),token,1,1);
        return -1;
    }
    int length = ntohl(p_req->_length);

    if ( length != proto_header_len)
    {
        tlogger::instance()->log("htbtp",fsk::level_t::debug_level(),token,2,1);
        return -1;
    }

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

    proto_htbt::pack_resp_v1(resp);
	return 0;
}

