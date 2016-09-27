
#include "video_get_leader.h"
#include "tigress_conf.h"

video_get_leader::video_get_leader():_vwm(NULL),_vwr(NULL),_acpter(NULL)
{

}

video_get_leader::~video_get_leader()
{
	if (_vwm != NULL)
	{
		delete _vwm;
		_vwm = NULL;
	}
	if (_vwr != NULL)
	{
		delete _vwr;
		_vwr = NULL;
	}
	if (_acpter != NULL)
	{
		delete _acpter;
		_acpter = NULL;
	}
	
}

int video_get_leader::start(string& res)
{
	int ret = 0;

	_vwm = new video_worker_manager;
	_vwr = new video_worker_register(_vwm);
	//_acpter = new netsvc::epoll_accepter<video_accept_handler>;
	_acpter = new netsvc::epoll_accepter<video_accept_handler_new>;

	ret = _vwr->regist_worker(res);
	if (0 != ret)
	{
		res = "receptor start fail when regist woker!";
		return -1;
	}

	int port=0, num=0;
	ret |= tigress_conf::get_instance()->get_integer_value("receptor", "upload_port", port);
	ret |= tigress_conf::get_instance()->get_integer_value("receptor", "thread_num", num);
	if ( 0!= ret)
	{
		res = "receptor read configure file fail!";
		return -1;
	}

	ret = _acpter->start(port, num, (void*)_vwm);
	if (0 != ret)
	{
		res = "receptor start fail when start netsvc!";
	}

	return ret;
}


