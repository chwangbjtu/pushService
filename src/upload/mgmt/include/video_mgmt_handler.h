
#ifndef __VIDEO_MGMT_HANDLER__
#define __VIDEO_MGMT_HANDLER__

#include "tcp_service.h"

const static unsigned int MAX_MGMT_HEADER_SIZE = 4096;

class video_mgmt_handler:public netsvc::epoll_handler
{
public:
	video_mgmt_handler();
	virtual ~video_mgmt_handler();

	virtual int handle_open(void *arg);
	virtual int handle_send(void);
	virtual int handle_recv(void);
	virtual int handle_close(void);
	virtual int handle_run(time_t tm);
private:
	std::string _recv;
	std::string _resp;
	ssize_t _send_pos;
};

#endif
