#include <arpa/inet.h>
#include "dbg.h"
#include "proto_constant.h"
#include "proto_process.h"
#include "proto_dispatcher.h"


proto_dispatcher* proto_dispatcher::_instance = NULL;

proto_dispatcher::proto_dispatcher()
{
    proto_login * pl = new proto_login();
    proto_htbt * ph = new proto_htbt();
}

proto_dispatcher::~proto_dispatcher()
{
}
proto_dispatcher* proto_dispatcher::instance()
{
	if(_instance == NULL)
		_instance = new proto_dispatcher();
	return _instance;
}

void proto_dispatcher::reg(unsigned int cmd,fp_base_handler* proto)
{
	_dispatcher.insert(make_pair(cmd,proto));
}

int proto_dispatcher::process(string& req, unsigned int ip,int threadid,int& id,string& resp)
{
    const char* s = req.data();
    unsigned int type = ntohs(*((unsigned short*)(s+proto_header_type_offset))) << 16
               | ntohs(*(unsigned short*)(s + proto_header_version_offset));
    //int length = ntohl(*((unsigned int*)(s+proto_header_length_offset)));
    //

    map<unsigned int,fp_base_handler*>::iterator it = _dispatcher.begin();
    
	map<unsigned int,fp_base_handler*>::iterator iter = _dispatcher.find(type);

	if ( iter != _dispatcher.end())
	{
		//return iter->second->process(hr._req._map_params,ip,resp);
		return iter->second->process(req,ip,threadid,id,resp);
	}
    DBG_INFO("");
	
	return -1;
}

