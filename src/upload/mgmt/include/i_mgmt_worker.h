
#ifndef __I_mgmt__WORKER__
#define __I_mgmt__WORKER__

#include <string>
#include "http_def.h"
#include "tigress_logger.h"

class i_mgmt_worker
{
public:
	i_mgmt_worker() {}
	virtual ~i_mgmt_worker() {}
	//virtual int procrss_header(http_t& req);
	//virtual int process_body(string& body);
	virtual int process(fs::request_t& req, std::string& resp) {return -1;}
};

#endif
