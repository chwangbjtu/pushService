
#include "tigress_leader.h"

using namespace std;

tigress_leader* tigress_leader::_instance=new tigress_leader;

//tigress_leader::tigress_leader()
//{

//}

tigress_leader::~tigress_leader()
{
	if (_vgl != NULL)
	{
		delete _vgl;
		_vgl = NULL;
	}
	if (_inl != NULL)
	{
		delete _inl;
		_inl = NULL;
	}
	if (_sl != NULL)
	{
		delete _sl;
		_sl = NULL;
	}
	if (_ml != NULL)
	{
		delete _ml;
		_ml = NULL;
	}
	/*if (_vpl != NULL)
	{
		delete _vpl;
		_vpl = NULL;
	}*/
}

tigress_leader* tigress_leader::get_instance()
{
	if (_instance == NULL)
	{
		_instance = new tigress_leader;//线程不安全的，但是程序不应该运行到这里。
	}

	return _instance;
}

int tigress_leader::start(std::string& res)
{
	_vgl = new video_get_leader;
	if (0 != _vgl->start(res))
	{
		return -1;
	}
	_inl = new info_leader;
	if (0 != _inl->start(res))
	{
		return -1;
	}
	_sl = new sync_leader;
	if (0 != _sl->start(res))
	{
		return -1;
	}
	_ml = new mgmt_leader;
	if (0 != _ml->start(res))
	{
		return -1;
	}
	/*_vpl = new video_post_leader;
	if (0 != _vpl->start(res))
	{
		return -1;
	}*/

	return 0;
}

int tigress_leader::query_info(string& taskid, file_info*& info)
{
	return _inl->query_info(taskid, info);
}

int tigress_leader::get_new_fileinfo(meta_data& md, file_info*& fin)
{
	return _inl->get_new_fileinfo(md, fin);
}

//arg is file_info* 
int tigress_leader::flush_to_disk(void* arg, char* pstart, int len)
{
	_sl->flush_to_disk(arg, pstart, len);
	return 0;
}

int tigress_leader::flush_meta_to_disk(void* arg)
{
	_sl->flush_meta_to_disk(arg);
	return 0;
}

int tigress_leader::delete_info(string& taskid, string& val)
{
	return _inl->delete_info(taskid, val);
}

int tigress_leader::query_version(string& val)
{
	val = TIGRESS_VERSION;
	return 0;
}

int tigress_leader::query_stats(string& taskid,string& result)
{
	return _inl->query_stats(taskid,result);
}

int tigress_leader::query_stats(string& result)
{
	return _inl->query_stats(result);
}

//
bool tigress_leader::upload_send_state(string& taskid,int state)
{
	return _inl->upload_send_state(taskid, state);
}

