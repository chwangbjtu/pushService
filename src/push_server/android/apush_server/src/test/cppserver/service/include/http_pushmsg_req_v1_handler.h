#ifndef __HTTP_PUSHMSG_REQ_V1_HANDLER_H
#define __HTTP_PUSHMSG_REQ_V1_HANDLER_H

#include "http_cmd.h"

class http_pushmsg_req_v1_handler: public http_cmd
{
public:
	virtual int process(const fs::http_request& hr,unsigned int ip,string& resp);
private:
	//int unpack(const multimap<string,string>& req,android_req_struct_t& req_struct);
};

#endif//__HTTP_PUSHMSG_REQ_V1_HANDLER_H

