#ifndef __FP_LOGIN_REQ_V1_HANDLER_H
#define __FP_LOGIN_REQ_V1_HANDLER_H

#include "fp_base_handler.h"

class fp_login_req_v1_handler: public fp_base_handler
{
public:
        virtual int process(string& req,unsigned int ip,int threadid,int& id,string& token,string& resp);
        //int unpack(const multimap<string,string>& req,android_req_struct_t& req_struct);
};

#endif//__FP_LOGIN_REQ_V1_HANDLER_H
