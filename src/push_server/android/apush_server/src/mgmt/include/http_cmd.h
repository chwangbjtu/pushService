#ifndef __HTTP_CMD_H
#define __HTTP_CMD_H
#include <string>
#include <map>

#include "http_request.h"

using namespace std;
class http_cmd
{
public:

	enum
	{
		return_ok,
		req_invalid
	};
	
	http_cmd();
	
	//virtual int process(const multimap<string,string>& req,unsigned int ip,string& resp){return -1;}
	virtual int process(const fs::http_request& hr,unsigned int ip,string& resp){return -1;}
	
	virtual ~http_cmd(){};
protected:

	int pack(string& msg,string& resp);
};

#endif //__HTTP_CMD_H

