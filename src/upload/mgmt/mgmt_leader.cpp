
#include "tigress_conf.h"
#include "mgmt_leader.h"

mgmt_leader::mgmt_leader() : _mwm(NULL), _mwr(NULL), _acpter(NULL)
{

}

mgmt_leader::~mgmt_leader()
{
	if (NULL == _mwm)
	{
		delete _mwm;
		_mwm = NULL;
	}
	if (NULL == _mwr)
	{
		delete _mwr;
		_mwr = NULL;
	}
	if (NULL == _acpter)
	{
		delete _acpter;
		_acpter = NULL;
	}
}

int mgmt_leader::start(string& res)
{
	int port=0, num=0;

	_mwm = new mgmt_worker_manager;
	_mwr = new mgmt_worker_register;
	_acpter = new netsvc::epoll_accepter<video_mgmt_handler>;

	if (0 != _mwr->regist_worker(_mwm, res))
	{
		return -1;
	}

	tigress_conf::get_instance()->get_integer_value("mgmt", "mgmt_port", port);
	tigress_conf::get_instance()->get_integer_value("mgmt", "thread_num", num);
	if (0 != _acpter->start(port, num, (void*)_mwm))
	{
		res = "mgmt start fail when start netsvc!";
		return -1;
	}

	return 0;
}
