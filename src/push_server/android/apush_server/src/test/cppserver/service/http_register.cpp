#include "http_register.h"

#include "http_dispatcher.h"
//#include "proto_constant.h"
#include "http_pushmsg_req_v1_handler.h"

bool http_register::init = false;

int http_register::start()
{
	if ( !init)
	{
		init = true;

        //http_dispatcher::instance()->reg("/parse",new fp_parse_req_v1_handler());
        http_dispatcher::instance()->reg("/push_msg",new http_pushmsg_req_v1_handler());
		
	}
	return 0;
}

