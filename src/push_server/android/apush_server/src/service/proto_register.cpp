#include "proto_register.h"
#include "dbg.h"
#include "fp_login_req_v1_handler.h"
#include "fp_htbt_req_v1_handler.h"
#include "fp_push_req_v1_handler.h"
#include "proto_dispatcher.h"
#include "proto_constant.h"

bool proto_register::init = false;

int proto_register::start()
{
	if ( !init)
	{
		init = true;

        unsigned int type_version = proto_login_req;
        type_version = type_version << 16 | version1;
        proto_dispatcher::instance()->reg(type_version,new fp_login_req_v1_handler());
        type_version = proto_htbt_req;
        type_version = type_version << 16 | version1;
        proto_dispatcher::instance()->reg(type_version,new fp_htbt_req_v1_handler());
		type_version = proto_push_req;
		type_version = type_version << 16 | version1;
		proto_dispatcher::instance()->reg(type_version,new fp_push_req_v1_handler());
		
	}
	return 0;
}

