
#include "k_str.h"
#include "json.h"
#include "tigress_leader.h"
#include "tigress_logger.h"
#include "mgmt_delete.h"

mgmt_delete::mgmt_delete()
{

}

mgmt_delete::~mgmt_delete()
{

}

int mgmt_delete::process(fs::request_t& req, std::string& resp)
{
	std::string taskid, tmp;
	
	pandaria::json jn;
	if (-1 == req.get_param("taskid", taskid))
	{
		jn.add("ret","1");
		jn.add("info","not find taskid");
		resp = jn.to_formated_str();
		return 0;
	}
	//fileid = str2upper(tmp);

	string val;
	int ret = tigress_leader::get_instance()->delete_info(taskid, val);
	if (ret < 0)
	{
		jn.add("ret","0");
		jn.add("info",val);//the file to delete does not exits";
		resp = jn.to_formated_str();
	}
	else if (ret == 0)
	{
		KINFO("the file %s has been deleted by mgmt command", taskid.c_str())
		jn.add("ret","0");//the file has been successfully deleted";
		resp = jn.to_formated_str();
	}
	else
	{
		jn.add("ret","1");
		jn.add("info",val);// need to waite;
		resp = jn.to_formated_str();
	}

	return 0;
}
