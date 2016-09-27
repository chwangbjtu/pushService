
#ifndef __MGMT_NULL__
#define __MGMT_NULL__

#include "i_mgmt_worker.h"

class mgmt_null:public i_mgmt_worker
{
public:
	mgmt_null();
	virtual ~mgmt_null();
	virtual int process(fs::request_t& req, std::string& resp);
};

#endif
