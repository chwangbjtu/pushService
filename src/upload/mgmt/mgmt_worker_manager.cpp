
#include "mgmt_worker_manager.h"

mgmt_worker_manager::mgmt_worker_manager()
{

}

mgmt_worker_manager::~mgmt_worker_manager()
{

}

int mgmt_worker_manager::get_response(string& req, string& resp)
{
	_req_header.reset();
	_resp_t.reset();

	if (0 != _http_req.parse((char*)req.c_str(), req.size(), _req_header))
	{
		return -1;
	}
	string url = _req_header.get_url();
	if (url != "/tigress/mgmt")
	{
		return -1;
	}

	i_mgmt_worker* mw = NULL;
	if (0 != get_worker(_req_header, mw))
	{
		return -1;
	}
	string str;
	mw->process(_req_header, str);
	_resp_t._version = "1.1";
	_resp_t._code = "200";
	_resp_t._code_info = "OK";
	_resp_t._content = str;
	if (-1 == _http_resp.pack(_resp_t, resp))
	{
		return -1;
	}

	return 0;
}

int mgmt_worker_manager::get_worker(fs::request_t& req, i_mgmt_worker*& pworker)
{
	pworker = NULL;
	string cmd;

	if (-1 == req.get_param("cmd", cmd))
	{
		return -1;
	}

	map<string, i_mgmt_worker*>::iterator iter = _cmd_workers.find(cmd);
	if (iter != _cmd_workers.end())
	{
		pworker = iter->second;
	}
	else
	{
		pworker = _cmd_workers["_null"];
	}

	return 0;

}

int mgmt_worker_manager::register_worker(string res, i_mgmt_worker* mw)
{
	pair<map<string, i_mgmt_worker*>::iterator, bool> ins;
	int ret = 0;

	ins = _cmd_workers.insert( make_pair(res, mw) );
	if (!ins.second)
		ret = -1;

	return ret;
}
