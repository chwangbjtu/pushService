
#ifndef __VIDEO_GET_LEADER__
#define __VIDEO_GET_LEADER__

#include "tcp_service.h"
#include "video_accept_handler.h"
#include "video_accept_handler_new.h"
#include "video_worker_manager.h"
#include "video_worker_register.h"

class video_get_leader
{
	public:
		video_get_leader();
		~video_get_leader();

		int start(string& res);

	private:
		video_worker_manager* _vwm;
		video_worker_register* _vwr;
		netsvc::epoll_accepter<video_accept_handler_new> *_acpter;
};

#endif
