
#ifndef __MGMT_QUERYVERSION__
#define __MGMT_QUERYVERSION__

#include "i_mgmt_worker.h"

class mgmt_queryversion:public i_mgmt_worker
{
public:
	mgmt_queryversion();
	virtual ~mgmt_queryversion();
	virtual int process(fs::request_t& req, std::string& resp);
};

#endif
