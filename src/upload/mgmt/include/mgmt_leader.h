
#ifndef __MGMT_LEADER__
#define __MGMT_LEADER__

#include "mgmt_worker_manager.h"
#include "mgmt_worker_register.h"
#include "video_mgmt_handler.h"

class mgmt_leader
{
public:
	mgmt_leader();
	~mgmt_leader();
	int start(string& res);
private:
	mgmt_worker_manager* _mwm;
	mgmt_worker_register* _mwr;
	netsvc::epoll_accepter<video_mgmt_handler> *_acpter;
};

#endif
