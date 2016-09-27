
#include "mgmt_worker_register.h"
#include "mgmt_null.h"
#include "mgmt_queryversion.h"
#include "mgmt_delete.h"
#include "mgmt_querystats.h"

mgmt_worker_register::mgmt_worker_register()
{

}

mgmt_worker_register::~mgmt_worker_register()
{

}

int mgmt_worker_register::regist_worker(mgmt_worker_manager* mwm, std::string& res)
{
	int ret = 0;

	ret |= mwm->register_worker("_null", new mgmt_null);
	ret |= mwm->register_worker("delete", new mgmt_delete);
	ret |= mwm->register_worker("queryversion", new mgmt_queryversion);
	ret |= mwm->register_worker("querystats", new mgmt_querystats);

	if (0 != ret)
	{
		res = "mgmt worker regist fail!\n";
	}

	return ret;
}
