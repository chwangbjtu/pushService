
#include "video_worker_manager.h"

video_worker_manager::video_worker_manager()
{

}

video_worker_manager::~video_worker_manager()
{

}

int video_worker_manager::register_path_worker(string path, i_accept_worker* path_worker)
{
	//map<string, i_accept_worker*>::iterator iter = _path_workers.find(path);
	pair<map<string, i_accept_worker*>::iterator, bool> ins;
	int ret = 0;

	//if (iter == _path_workers.end())
	//{
	ins = _path_workers.insert( make_pair(path, path_worker) );
	if (!ins.second)
	{
		ret = -1;
	}
	//}

	return ret;
}

int video_worker_manager::get_accept_worker(request_t& http_req, i_accept_worker*& _pworker)
{
	int ret = -1;
	_pworker = NULL;

	//string path = (const_cast<http_request*>(http_req))->get_url();
	string path = http_req.get_url();
	if (http_req._method == "OPTIONS")
	{
		path = "OPTIONS" + path;
	}
	map<string, i_accept_worker*>::iterator iter = _path_workers.find(path);

	if (iter != _path_workers.end())
	{
		_pworker = iter->second->get_clone();
		if (NULL != _pworker)
		{
			ret = 0;
		}
	}

	return ret;
}

/*
int video_worker_manager::process(request_t& http_req, string& resp)
{
	
	int ret = -1;
	_pworker = NULL;

	string path = http_req.get_url();
	if (http_req._method == "OPTIONS")
	{
		path = "OPTIONS" + path;
	}
	map<string, i_accept_worker*>::iterator iter = _path_workers.find(path);

	if (iter != _path_workers.end())
	{
		i_accept_worker* pworker = iter->second->get_clone();
		if (NULL != pworker)
		{
			ret = pworker->process();
		}
	}
	

	
	return ret;

}
*/

