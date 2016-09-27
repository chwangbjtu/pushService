
#include "tigress_leader.h"
#include "mgmt_queryversion.h"

mgmt_queryversion::mgmt_queryversion()
{

}

mgmt_queryversion::~mgmt_queryversion()
{

}

int mgmt_queryversion::process(fs::request_t& req, std::string& resp)
{
	string str;

	KINFO("an mgmt command of queryversion")
	tigress_leader::get_instance()->query_version(str);
	resp = "return=ok\nversion=" + str;

	return 0;
}
