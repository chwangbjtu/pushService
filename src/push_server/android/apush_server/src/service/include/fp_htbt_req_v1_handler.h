#ifndef __FP_HTBT_REQ_V1_HANDLER_H
#define __FP_HTBT_REQ_V1_HANDLER_H

#include "fp_base_handler.h"

class fp_htbt_req_v1_handler: public fp_base_handler
{
public:
        virtual int process(string& req,unsigned int ip,int threadid,int& id,string& token,string& resp);
private:
        //int unpack(const multimap<string,string>& req,android_req_struct_t& req_struct);
};

#endif//__FP_HTBT_REQ_V1_HANDLER_H
