#include <arpa/inet.h>
#include "dbg.h"
#include "proto_constant.h"
#include "proto_process.h"
#include "tlogger.h"
#include "proto_dispatcher.h"
#include "util.h"


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

int proto_dispatcher::process(string& req, unsigned int ip,int threadid,int& id,string& token,string& resp)
{
    const char* s = req.data();
    unsigned short header_type = ntohs(*((unsigned short*)(s+proto_header_type_offset)));
    unsigned short header_version = ntohs(*(unsigned short*)(s + proto_header_version_offset));
    unsigned int type = ntohs(*((unsigned short*)(s+proto_header_type_offset))) << 16
               | ntohs(*(unsigned short*)(s + proto_header_version_offset));
    //int length = ntohl(*((unsigned int*)(s+proto_header_length_offset)));
    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, type: %x,version: %d", util::get_conn_id(threadid, id), token.c_str(), header_type, header_version);
    
	map<unsigned int,fp_base_handler*>::iterator iter = _dispatcher.find(type);

	if ( iter != _dispatcher.end())
	{
		//return iter->second->process(hr._req._map_params,ip,resp);
		return iter->second->process(req,ip,threadid,id,token,resp);
	}
	
	return -1;
}

