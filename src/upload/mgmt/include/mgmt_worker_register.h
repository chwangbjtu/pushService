
#ifndef __MGMT_WORKER_REGISTER__
#define __MGMT_WORKER_REGISTER__

#include <string>
#include "mgmt_worker_manager.h"

class mgmt_worker_register
{
public:
	mgmt_worker_register();
	~mgmt_worker_register();
	int regist_worker(mgmt_worker_manager* mwm, std::string& res);
};

#endif
