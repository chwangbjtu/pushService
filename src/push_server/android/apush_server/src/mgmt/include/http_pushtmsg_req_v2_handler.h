#ifndef __HTTP_PUSHTMSG_REQ_V2_HANDLER_H
#define __HTTP_PUSHTMSG_REQ_V2_HANDLER_H

#include "http_cmd.h"

class http_pushtmsg_req_v2_handler: public http_cmd
{
public:
	virtual int process(const fs::http_request& hr,unsigned int ip,string& resp);
private:
	//int unpack(const multimap<string,string>& req,android_req_struct_t& req_struct);
};

#endif//__HTTP_PUSHTMSG_REQ_V2_HANDLER_H

