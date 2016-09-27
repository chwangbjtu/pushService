
#ifndef __VIDEO_WORKER_REGISTER__
#define __VIDEO_WORKER_REGISTER__

#include <string>
#include "video_worker_manager.h"

class video_worker_register
{
	public:
		video_worker_register();
		video_worker_register(video_worker_manager* vwm);/////
		~video_worker_register();

		int regist_worker(string& res);
	private:
		video_worker_manager* _vwm;
};

#endif
