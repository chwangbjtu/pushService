
#ifndef __VIDEO_WORKER_MANAGER__
#define __VIDEO_WORKER_MANAGER__

#include <map>
#include <string>
#include "i_accept_worker.h"

class video_worker_manager
{
	public:	
		video_worker_manager();
		~video_worker_manager();

		int register_path_worker(string path, i_accept_worker * path_worker);
		int get_accept_worker(request_t& http_req, i_accept_worker*& aw);

	private:

		map<string, i_accept_worker*> _path_workers;

};

#endif
