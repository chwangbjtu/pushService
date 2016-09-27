#ifndef __HTTP_DISPATCHER_H
#define __HTTP_DISPATCHER_H
#include <map>
#include <string>
#include "http_cmd.h"
using namespace std;

class http_dispatcher
{
public:
	~http_dispatcher();
	static http_dispatcher* instance();

	void reg(string ,http_cmd* proto);
	
	virtual int process(string&req, unsigned int ip,string& resp);
private:
	http_dispatcher();
private:
	static http_dispatcher* _instance;
	map<string,http_cmd*> _dispatcher;//key=(proto_type<< 16 | proto_version)
};

#endif//__HTTP_DISPATCHER_H

