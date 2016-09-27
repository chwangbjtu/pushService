
#include <sstream>
#include <sys/types.h>
#include <dirent.h>
#include "data_manager.h"
#include "tigress_leader.h"
#include "tigress_logger.h"
#include "tigress_conf.h"
#include "meta_file.h"
#include "ret_code.h"
#include "md5_mgr.h"
//#include "http_response.h"
#include "json.h"

#include "msg_cmd_base.h"
#include "msg_manager.h"


data_manager::data_manager():_delay_time(60*60*6), _pm(NULL)
{
	//delay_time=60*60*24;
	//pthread_mutex_init(&_mutex_loading,NULL);
}

data_manager::data_manager(int d):_delay_time(d), _pm(NULL)
{
	//pthread_mutex_init(&_mutex_loading,NULL);
}

int data_manager::init(string& res)
{
	int dt = 1000000000;
	if (0 != tigress_conf::get_instance()->get_integer_value("info_manager", "delay_timeout", dt))
	{
		res = "data_manager read configure file fail";
		return -1;
	}

	_delay_time = dt;
	_pm = new path_manager();
	if (NULL == _pm || 0 != _pm->init(res))
	{
		return -1;
	}

	pthread_mutex_init(&_mutex_loading,NULL);

	return 0;
}

data_manager::~data_manager()
{
	if (_pm != NULL)
	{
		delete _pm;
		_pm = NULL;
	}
	pthread_mutex_destroy(&_mutex_loading);
}

//uhash is :userid+hashid
int data_manager::query_info(string& uhash, file_info*& info)
{
	map<string,file_info*>::iterator iter;
	int ret = -1;
	pthread_mutex_lock(&_mutex_loading);
	iter = _loading_info.find(uhash);
	if (iter != _loading_info.end())
	{
		info = iter->second;
		ret = 0;
	}
	else
	{
		info = NULL;
	}
	pthread_mutex_unlock(&_mutex_loading);

	return ret;
}

int data_manager::dispatch_info(string& taskid, file_info* info)
{
	pair<map<string,file_info*>::iterator,bool> ret;

	pthread_mutex_lock(&_mutex_loading);
	ret = _loading_info.insert(pair<string,file_info*>(taskid, info));
	pthread_mutex_unlock(&_mutex_loading);


	if (ret.second)
	{
		//KINFO("the file %s prog to upload", info->_meta._file_id.c_str())
		return 0;
	}
	else
	{
		//KWARN("the file %s prog to upload fail", info->_meta._file_id.c_str())
		return -1;
	}
}

int data_manager::update_info(string& taskid, file_info* info)
{
	return 0;//not use now
}

int data_manager::delete_info(string& taskid, string& val)
{
	int ret = 0;
	map<string,file_info*>::iterator iter;

	pthread_mutex_lock(&_mutex_loading);
	iter = _loading_info.find(taskid);
	if (iter != _loading_info.end())
	{
		int result = iter->second->file_delete();
		if (0 >= result)
		{
			delete iter->second;
			_loading_info.erase(iter);
			ret = 0; //delete success
			if (result == 0)
				val = "the file has been successfully deleted";
			else
				val = "the file has been deleted but some error occur";
		}
		else if (result > 0)
		{
			ret = 1; //need to wait
			val  = "need to wait";
		}
	}
	else
	{
		val = "the file to delete does not exits";
		KWARN("delete a file %s info that does not exist", taskid.c_str())
		ret = -1;
	}
	pthread_mutex_unlock(&_mutex_loading);

	return ret;
}

int data_manager::delay_aging(map<string, file_info*> &aging_info)
{
	/*
	map<string,file_info*>::iterator iter;
	pair<map<string,file_info*>::iterator, bool> ret;
	//time_t now = time(NULL);

	pthread_mutex_lock(&_mutex_loading);
	for (iter = _loading_info.begin();iter != _loading_info.end();)
	{
		if (iter->second->file_aging(_delay_time))
		{
			ret = aging_info.insert(pair<string,file_info*>(iter->first, iter->second));
			if (!ret.second)
				KERROR("the file %s aging treat error", iter->first.c_str())
			_loading_info.erase(iter++);
		}
		else 
		{
			++iter;
		}
	}
	pthread_mutex_unlock(&_mutex_loading);
	*/
	return 0;
}

int data_manager::get_new_fileinfo(meta_data& md, file_info*& fin)
{
	string path;
	int ret = -1;

	if(0 == _pm->get_file_path(md._length, path))
	{
		file_info* f = new file_info();
		if (0 == f->file_init(path, md) && 0 == dispatch_info(md._uhash, f))
		{
			KINFO("the file %s prog to upload", md._uhash.c_str())
			ret = 0;
			fin = f;
		}
		else
		{
			KWARN("the file %s prog to upload fail", md._uhash.c_str())
			delete f;
		}
	}
	else
	{
		KERROR("the file %s prog to upload fail for having no disk space with length %lld", md._uhash.c_str(), md._length)
	}

	return ret;
}

int data_manager::get_info_count()
{
	int ret = -1;
	pthread_mutex_lock(&_mutex_loading);
	ret = _loading_info.size();
	pthread_mutex_unlock(&_mutex_loading);

	return ret;
}

int data_manager::reload()
{
	string path, name;
	tigress_conf::get_instance()->get_string_value("info_manager", "file_paths", path);
	_pm->get_file_path(0, path);

	DIR* d = opendir(path.c_str());
	struct dirent* dt = NULL;

	if (NULL == d)
	{
		KERROR("the reload path %s can not open", path.c_str())
		return -1;
	}

	while ((dt = readdir(d)) != NULL)
	{
		if (strncmp(dt->d_name, ".", 1) == 0)
			continue;
		//if (dt->d_type == DT_REG)
		{
			char* sr = strstr(dt->d_name, ".meta");
			if (sr != NULL && (*(sr + 5)) == '\0')
			{
				name = path + dt->d_name;
				reload_single_file(name);
			}
		}
	}
	closedir(d);

	get_send_metas();

	map<string,file_info*>::iterator iter = _loading_info.begin();
	int i =1;
	for(;iter!=_loading_info.end();iter++)
	{
		i++;
		KINFO("load file %d",i);
		KINFO("load file : %s",iter->first.data())
	}

	return 0;
}

int data_manager::reload_single_file(string& fname)
{
	meta_file mf;
	meta_data md;

	if (0 != mf.parse_meta_data(md, fname))
	{
		KERROR("the file %s reload fail with reason meta_data parse fail", fname.c_str())
		return -1;
	}

	file_info* fin = new file_info;
	if (0 != fin->file_reload(md, fname) || 0 != dispatch_info(md._uhash, fin))
	{
		KERROR("the file %s reload fail with reason video file relaod fail", fname.c_str())
		delete fin;
		return -1;
	}

	return 0;
}

int data_manager::get_send_metas()
{
	map<string,file_info*>::iterator iter;

	pthread_mutex_lock(&_mutex_loading);
	for (iter = _loading_info.begin();iter != _loading_info.end();++iter)
	{
		if ( iter->second->send_not_over())
		{
			if ( (iter->second->_meta._send_to_maze & send_upload_begin) == 0)
			{
				string resp2server;
				pack("upload_start",iter->second->_meta,resp2server);

				msg_cmd_base *pcmd = new msg_cmd_base(1,send_upload_begin,iter->second->_meta._uhash,resp2server);
				msg_manager::instance()->dispatch(pcmd);
			}

			if ( (iter->second->_meta._send_to_maze & send_upload_finish)== 0)
			{
				string resp2server;
				pack("upload_finish",iter->second->_meta,resp2server);

				msg_cmd_base *pcmd = new msg_cmd_base(1,send_upload_finish,iter->second->_meta._uhash,resp2server);
				msg_manager::instance()->dispatch(pcmd);
			}
			/*
			if ( (iter->second->_meta._send_to_maze & send_transcode) == 0)
			{
				string resp2server;
				pack("transcode_add",iter->second->_meta,resp2server);

				msg_cmd_base *pcmd = new msg_cmd_base(1,send_transcode,iter->second->_meta._task_id,resp2server);
				msg_manager::instance()->dispatch(pcmd);
			}
			*/
		}
	}
	
	
	pthread_mutex_unlock(&_mutex_loading);
}

int data_manager::query_stats(string& tid,string& result)
{
	map<string,file_info*>::iterator iter;
	
	pthread_mutex_lock(&_mutex_loading);
	iter = _loading_info.find(tid);
	if ( iter != _loading_info.end())
	{
		iter->second->file_stat_new(result);
	}
	else
	{
		pandaria::json jn;
		jn.add("ret","1");
		jn.add("info","not find taskid");
		result = jn.to_formated_str();
	}
	pthread_mutex_unlock(&_mutex_loading);

	return 0;
}

int data_manager::query_stats(string& result)
{
	map<string,file_info*>::iterator iter;
	
	pthread_mutex_lock(&_mutex_loading);
	iter = _loading_info.begin();
	pandaria::json jng;
	for ( ;iter != _loading_info.end();iter++)
	{
		pandaria::json jn;
		jn.add("taskid",iter->second->_meta._task_id);
		jn.add("fileid",iter->second->_meta._file_id);
		jn.add("filename",iter->second->_meta._file_name);
		jn.add("filelength",iter->second->_meta._length);
		jn.add("offset",iter->second->_meta._offset);
		jn.add("uid",iter->second->_meta._uid);
		jn.add("hashid",iter->second->_meta._hash_id);
		jn.add("createtime",(int)iter->second->_meta._create_time);
		jn.add("lasttime",(int)iter->second->_meta._last_time);
		jn.add("sendtomaze",iter->second->_meta._send_to_maze);
		jn.add("ret","0");

		jng.append("info",jn);
	}

	result = jng.to_formated_str();
	pthread_mutex_unlock(&_mutex_loading);

	/*
	string tmp = "";
	stringstream sstr;
	sstr<<"total size ";
	map<string,file_info*>::iterator iter;

	pthread_mutex_lock(&_mutex_loading);
	sstr<<_loading_info.size();
	sstr<<"\r\nfileid,filename,status,length,upload_offset\r\n";
	result += sstr.str();
	for (iter = _loading_info.begin();iter != _loading_info.end();++iter)
	{
		(*iter).second->file_stat(tmp);
		result += tmp;
		result += "\r\n";
		tmp.clear();
	}
	pthread_mutex_unlock(&_mutex_loading);
	*/
	return 0;
}

//
bool data_manager::upload_send_state(string& taskid,int state)
{
	map<string,file_info*>::iterator iter;
	int ret = false;
	pthread_mutex_lock(&_mutex_loading);
	iter = _loading_info.find(taskid);
	if (iter != _loading_info.end())
	{
		iter->second->_meta._send_to_maze = (iter->second->_meta._send_to_maze | state);
		ret = true;
	}
	else
	{
		KERROR("not find taskid %s",taskid.data());
	}
	pthread_mutex_unlock(&_mutex_loading);

	return ret;
}

//启动时发现未发送成功的文件，重新发送
int data_manager::pack(const string type,meta_data& data,string& resp)
{
	pandaria::json jn;
	stringstream st;
	string tmp;

	jn.add("task_id",data._task_id);
	tigress_conf::get_instance()->get_string_value("info_manager", "file_paths", tmp);
	tmp = tmp + data._task_id + ".down";
    string md5str;
    md5_mgr::instance()->get_md5str(tmp,md5str);
	jn.add("file",tmp);
	jn.add("file_name",data._file_name);
	tmp.clear();
	st<<data._length;
	st>>tmp;
	jn.add("file_size",tmp);
	string url;
	tigress_conf::get_instance()->get_string_value("visitor", "play_path", url);
	url = url + data._task_id + ".down" + "#md5=" + md5str;
	jn.add("file_url",url);
	jn.add("uid",data._uid);
	jn.add("hashid",data._hash_id);

	//string str = "close";
	string str = "keep-alive";

	tmp = jn.to_formated_str();
	
	fs::http_request http_req;
	fs::request_t req_t;


	req_t._method = "POST";
	if ( type == cmd_upload_start)
	{
		req_t._path = cmd_upload_start_path;
	}
	else if ( type == cmd_upload_finish)
	{
		req_t._path = cmd_upload_finish_path;
		jn.add("result","0");
	}
	else if ( type == cmd_transcode_add)
	{
		req_t._path = cmd_transcode_add_path;
	}
	req_t.add_message_header("connection", str);
	str = "text/plain;charset=UTF-8";
	req_t.add_message_header("Content-Type", str);

	//st<<data._length;
	//st>>tmp;
	
	//req_t.add_message_header("Content-Length", tmp);
	str = "null";
	req_t.add_message_header("Origin",str);
	str = "no-cache";
	req_t.add_message_header("Pragma", str);
	req_t.add_message_header("Cache-Control", str);

	st.clear();
	tmp.clear();
	req_t._content = jn.to_formated_str();
	
	if (-1 == http_req.pack(req_t, resp))
	{
		resp = "";
	}

	return 0;
}


