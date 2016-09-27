
#ifndef __MGMT_WORKER_MANAGER__
#define __MGMT_WORKER_MANAGER__

#include <string>
#include <map>
#include "http_def.h"
#include "http_request.h"
#include "http_response.h"
#include "i_mgmt_worker.h"

using namespace std;

class mgmt_worker_manager
{
public:
	mgmt_worker_manager();
	~mgmt_worker_manager();

	int get_response(string& req, string& resp);
	int get_worker(fs::request_t& req, i_mgmt_worker*& pworker);

	int register_worker(string res, i_mgmt_worker* mw);
private:
	map<string, i_mgmt_worker*> _cmd_workers;
	fs::request_t _req_header;
	fs::response_t _resp_t;
	fs::http_request _http_req;
	fs::http_response _http_resp;
};

#endif
