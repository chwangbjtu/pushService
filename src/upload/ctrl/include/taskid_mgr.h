#ifndef __TASKID_MGR_H
#define __TASKID_MGR_H

#include <map>
#include "kmutex.h"
#include "klock.h"

using namespace std;

class taskid_mgr
{
public:
	~taskid_mgr(){}
	
	static taskid_mgr* instance();
	
	int get_taskid(string& uid,string& hashid,string& taskid);

	bool check(string& uid,string& hashid);

private:
	taskid_mgr();
	static taskid_mgr* _inst;
	multimap<string,string> _taskids;

	int _cnt;
	unsigned int _ip;

	fsk::kunique_mutex _mutex;
};

#endif//__TASKID_MGR_H

