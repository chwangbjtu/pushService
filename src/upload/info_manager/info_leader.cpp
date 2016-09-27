
#include "info_leader.h"
#include "tigress_conf.h"
#include "aging_treat.h"

info_leader::info_leader():_dm(NULL),_aging(NULL)
{
	_timer.initialize();
}

info_leader::~info_leader()
{
	if (NULL != _dm)
	{
		delete _dm;
		_dm = NULL;
	}

	if (NULL != _aging)
	{
		delete _aging;
		_aging = NULL;
	}

	_timer.destroy();
}

int info_leader::start(string& res)//, void*& dm)
{
	int ret = 0; // must be 0 here or second will fail
	_dm = new data_manager;
	_aging = new aging_treat(_dm);

	if (NULL == _dm || NULL == _aging || 0 != _dm->init(res))
	{
		res += "\ndata_manager start fail!";
		return -1;
	}

	int hour, min,interval;
	ret |= tigress_conf::get_instance()->get_integer_value("info_manager", "delay_interval", interval);
	ret |= tigress_conf::get_instance()->get_integer_value("info_manager", "delay_time_hour", hour);
	ret |= tigress_conf::get_instance()->get_integer_value("info_manager", "delay_time_minute", min);
	if (0 != ret)
	{
		res = "read delay aging configure fail!";
		return -1;
	}

	int delay = 0;
	time_t tv, tvd;
	tv = time(NULL);
	struct tm *st;
	st = localtime(&tv);
	st->tm_hour = hour;
	st->tm_min = min;
	tvd = mktime(st);

	if (tvd > tv)
	{
		delay = tvd - tv;
	}
	else
	{
		delay = 24*60*60 - tv + tvd;
	}

	_timer.schedule(_aging, fsk::ktimeval(delay, 0), fsk::ktimeval(interval, 0));

	_dm->reload(); // reload the local file
	return 0;
}


int info_leader::query_info(string& taskid, file_info*& info)
{
	return _dm->query_info(taskid, info);
}

int info_leader::delete_info(string& takid, string& val)
{
	return _dm->delete_info(takid, val);
}

int info_leader::get_new_fileinfo(meta_data& md, file_info*& fin)
{
	return _dm->get_new_fileinfo(md, fin);
}

int info_leader::query_stats(string& taskid,string& result)
{
	int ret = 0;
	if ( taskid.size() == 0)
	{
		ret = _dm->query_stats(result);
	}
	else
	{
		ret = _dm->query_stats(taskid,result);
	}
	
	return ret;
}

int info_leader::query_stats(string& result)
{
	return _dm->query_stats(result);
}

//
bool info_leader::upload_send_state(string& taskid,int state)
{
	return _dm->upload_send_state(taskid, state);
}

