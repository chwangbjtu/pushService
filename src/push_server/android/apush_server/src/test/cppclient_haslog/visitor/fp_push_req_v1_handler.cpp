#include <arpa/inet.h>
#include <stdlib.h>
#include <string>
#include "json/json.h"
#include "dbg.h"
#include "proto_constant.h"
#include "proto_process.h"
#include "fp_push_req_v1_handler.h"
#include "soc_mgr.h"


int fp_push_req_v1_handler::process(string& req,unsigned int ip,int threadid,int& id,string& resp)
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
    else if (length  == req.size())
    {
        sjson = req.substr(proto_header_len,length);
        req.clear();
    }

    DBG_INFO("%s",sjson.data());
    
    /*
    const char* s = req.data();
    int length = ntohl(*((unsigned int*)(s+proto_header_length_offset)));

	//接收的数据不止一个数据报文
	int msgid = -1;
    if ( length + proto_header_len < req.size())
    {
    	string sjson;
        sjson = req.substr(proto_header_len,length);
        string treq = req.substr(length+proto_header_len);
        req = treq;
    }
    else if (length + proto_header_len == req.size() && length > 0)
    {
        int * pmsgid = (int *)(s+proto_header_len);
		msgid = ntohl(*pmsgid);
        req.clear();
    }
    */

	string smsgid = "1126";
    soc_mgr::instance()->push_msgid(id,smsgid);
    

	return 0;
}

