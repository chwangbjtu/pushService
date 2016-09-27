#include "dbg.h"
#include "http_request.h"
//#include "proto_constant.h"
#include "http_dispatcher.h"

using  fs::http_request;

http_dispatcher* http_dispatcher::_instance = NULL;

http_dispatcher::http_dispatcher()
{
}

http_dispatcher::~http_dispatcher()
{
}
http_dispatcher* http_dispatcher::instance()
{
	if(_instance == NULL)
		_instance = new http_dispatcher();
	return _instance;
}

void http_dispatcher::reg(string cmd,http_cmd* proto)
{
	_dispatcher.insert(make_pair(cmd,proto));
}

int http_dispatcher::process(string& req, unsigned int ip,string& resp)
{
	http_request hr;

	if ( hr.parse(req.data(),req.size()) < 0) 
	{
		return -1;
	}

	string path = hr._req._path;

	map<string,http_cmd*>::iterator iter = _dispatcher.find(path);

	if ( iter != _dispatcher.end())
	{
		return iter->second->process(hr,ip,resp);
	}
	
	return -1;
}

