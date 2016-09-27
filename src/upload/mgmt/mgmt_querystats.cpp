
#include "tigress_leader.h"
#include "tigress_logger.h"
#include "mgmt_querystats.h"

mgmt_querystats::mgmt_querystats()
{

}

mgmt_querystats::~mgmt_querystats()
{

}

int mgmt_querystats::process(fs::request_t& req, std::string& resp)
{
	KINFO("an mgmt command of querystats")
	string taskid;
	req.get_param("taskid", taskid);
	tigress_leader::get_instance()->query_stats(taskid,resp);

	return 0;
}
