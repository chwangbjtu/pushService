
#ifndef __I_MGMT_QUERYSTATUS_H_
#define __I_MGMT_QUERYSTATUS_H_

#include "i_mgmt_worker.h"

class mgmt_querystats : public i_mgmt_worker
{
public:
	mgmt_querystats();
	virtual ~mgmt_querystats();

	virtual int process(fs::request_t& req, std::string& resp);
};

#endif
