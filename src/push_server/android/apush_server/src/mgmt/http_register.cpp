#include "http_register.h"

#include "http_dispatcher.h"
//#include "proto_constant.h"
#include "http_pushgmsg_req_v2_handler.h"
#include "http_pushmsg_req_v1_handler.h"
#include "http_pushtmsg_req_v2_handler.h"
#include "http_cancelpush_req_v1_handler.h"
#include "http_query_user_num_req_v1_handler.h"
#include "http_query_user_info_req_v1_handler.h"

bool http_register::init = false;

int http_register::start()
{
	if ( !init)
	{
		init = true;

        //http_dispatcher::instance()->reg("/parse",new fp_parse_req_v1_handler());
        http_dispatcher::instance()->reg("/push_msg",new http_pushmsg_req_v1_handler());
        http_dispatcher::instance()->reg("/pushg_msg",new http_pushgmsg_req_v1_handler());
        http_dispatcher::instance()->reg("/pusht_msg",new http_pushtmsg_req_v2_handler());
        http_dispatcher::instance()->reg("/cancel_msg",new http_cancelpush_req_v1_handler());
        http_dispatcher::instance()->reg("/query_user_info",new http_query_user_info_req_v1_handler());
        http_dispatcher::instance()->reg("/query_user_num",new http_query_user_num_req_v1_handler());
		
	}
	return 0;
}

