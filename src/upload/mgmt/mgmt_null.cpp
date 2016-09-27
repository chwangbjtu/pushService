
#include "mgmt_null.h"

mgmt_null::mgmt_null()
{

}

mgmt_null::~mgmt_null()
{

}

int mgmt_null::process(fs::request_t& req, std::string& resp)
{
	KERROR("an unknown mgmt command %s ", req.get_url().c_str())
	resp = "return=error\nerrorinfo=unknown command";
	return 0;
}
