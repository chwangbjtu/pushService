
#ifndef __MGMT_DELETE__
#define __MGMT_DELETE__

#include "i_mgmt_worker.h"

class mgmt_delete:public i_mgmt_worker
{
public:
	mgmt_delete();
	virtual ~mgmt_delete();
	//virtual int procrss_header(http_t& req);
	//virtual int process_body(string& body);
	virtual int process(fs::request_t& req, std::string& resp);
};

#endif
