
#include "video_worker_register.h"
#include "video_prog.h"
#include "video_upload.h"
#include "video_prog_new.h"
#include "video_upload_new.h"
#include "video_upload_options.h"
#include "video_upload_xml.h"

video_worker_register::video_worker_register(video_worker_manager* vwm):_vwm(vwm)
{

}

video_worker_register::~video_worker_register()
{

}

int video_worker_register::regist_worker(string& res)
{
	int ret = 0;

	ret |= _vwm->register_path_worker("/tigress/prog", new video_prog_new);
	ret |= _vwm->register_path_worker("/tigress/upload", new video_upload_new);
	ret |= _vwm->register_path_worker("/crossdomain.xml", new video_upload_xml);
	ret |= _vwm->register_path_worker("OPTIONS /tigress/upload", new video_upload_options);
	ret |= _vwm->register_path_worker("OPTIONS /tigress/prog", new video_upload_options);
	ret |= _vwm->register_path_worker("OPTIONS/tigress/upload", new video_upload_options);
	ret |= _vwm->register_path_worker("OPTIONS/tigress/prog", new video_upload_options);

	if ( 0 != ret)
	{
		res = "worker regist fail!\n";
	}

	return ret;
}

