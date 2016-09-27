#include<sstream>
#include "tigress_conf.h"
#include "taskid_mgr.h"

using namespace std;

taskid_mgr* taskid_mgr::_inst = NULL;
taskid_mgr* taskid_mgr::instance()
{
	if ( _inst == NULL)
		_inst = new taskid_mgr();
	return _inst;
}

taskid_mgr::taskid_mgr():_cnt(0)
{
	_ip = tigress_conf::get_instance()->get_int_value("local_host_ip");
}

int taskid_mgr::get_taskid(string& uid,string& hashid,string& taskid)
{
	fsk::kscope_lock<fsk::kunique_mutex> lck(_mutex);
	string key = uid;
	key.append(hashid);
	_cnt++;
	time_t now = time(NULL);
	stringstream sstr;
	sstr<<_ip<<now<<_cnt;
	sstr>>taskid;

	_taskids.insert(make_pair(key,taskid));

	return 0;
}

bool taskid_mgr::check(string& uid,string& hashid)
{
	bool res = true;
	fsk::kscope_lock<fsk::kunique_mutex> lck(_mutex);
	string key = uid;
	key.append(hashid);
	
	multimap<string,string>::iterator iter = _taskids.find(key);
	if ( iter == _taskids.end())
	{
		res = false;
	}

	return res;
}

