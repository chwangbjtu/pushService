
#include <vector>
#include <sstream>
#include "ret_code.h"
#include "util.h"
#include "tigress_leader.h"
#include "tigress_logger.h"
#include "video_prog_new.h"
#include "http_response.h"
#include "json.h"
#include "http_util.h"
#include "tigress_conf.h"
#include "taskid_mgr.h"
#include "msg_cmd_base.h"
#include "msg_manager.h"

video_prog_new::video_prog_new():i_accept_worker()
{
}

video_prog_new::~video_prog_new()
{
}

video_prog_new::video_prog_new(const video_prog_new& vp):i_accept_worker(vp)
{
}

i_accept_worker* video_prog_new::get_clone()
{
	return new video_prog_new(*this);
}

int video_prog_new::process_body(char const * const precv,long long len,string &task_id, string& resp)
{
	string body(precv,len);
	string res;
	string callback;
	int ret = -1;
	file_info* f_info;
	meta_data data;
	
	ret = parse_message(body, res, data,f_info,callback);
	if ( ret != 0 && res.size() != 0)
	{
		KINFO("parse_message error:%s",res.data());
	}
	task_id = data._task_id;

	ppack(ret,data,callback,f_info,resp);
	
	return ret;
}

//f_info 是在get_new_fileinfo中new 产生的，之前都的NULL
int video_prog_new::parse_message(string& s_body, string& resp, meta_data& data, file_info*& f_info,string& callback)
{
	string error_info;
	//string fileid, filename, filelen,taskid;
	string filelen;
	int ret=-1;
	pandaria::json jn;
	//meta_data md;

	int (*p_upper)(int)=toupper;

	multimap<string, string> tparam_pairs;
	parse_parameter(s_body.data(),s_body.size(),tparam_pairs);
	multimap<string, string>::iterator iter;
	iter = tparam_pairs.find("fileid");
	if ( iter != tparam_pairs.end() && iter->second.size() != 0)
	{
		data._file_id = iter->second;
		transform(data._file_id.begin(), data._file_id.end(), data._file_id.begin(),  p_upper);
	}

	iter = tparam_pairs.find("hashid");
	if ( iter != tparam_pairs.end() && iter->second.size() != 0)
	{
		data._hash_id = iter->second;
	}
	else
	{
		return -1;
	}

	iter = tparam_pairs.find("uid");
	if ( iter != tparam_pairs.end() && iter->second.size() != 0)
	{
		data._uid = iter->second;
	}
	else
	{
		return -1;
	}

	data._uhash = data._uid+data._hash_id;

	iter = tparam_pairs.find("filename");
	if ( iter != tparam_pairs.end() && iter->second.size() != 0)
	{
		data._file_name = iter->second;
	}
	else
	{
		return -1;
	}

	iter = tparam_pairs.find("callback");
	if ( iter != tparam_pairs.end() && iter->second.size() != 0)
	{
		callback = iter->second;
	}

	iter = tparam_pairs.find("filelength");
	if ( iter != tparam_pairs.end() && iter->second.size() != 0)
	{
		data._length = atoll(iter->second.c_str());
	}
	else
	{
		return -1;
	}

	if ( data._hash_id.size() == 0 || data._uid .size() == 0 || data._file_name.size() == 0 || data._length <= 0)
	{
		return -1;
	}

	data._key = util::instance()->get_key(data._task_id);
	//data = md;

	int res = check_uhash( data, f_info);

	return res;
}

//如果客户端上传基本信息时使用GET方式，才会调用本方法
int video_prog_new::process_header(request_t& http_req, string& uhash,string& resp)
{
	//string off, fid, taskid,uid,hashid,err,checksum;
	int ret = 0;
	meta_data data;

	string callback;
	string length = "0";
	
	http_req.get_param("fileid", data._file_id);
	http_req.get_param("hashid", data._hash_id);
	http_req.get_param("uid", data._uid);
	http_req.get_param("filename", data._file_name);
	http_req.get_param("callback", callback);
	http_req.get_param("filelength", length);

	data._length = atoll(length.c_str());

	if ( data._hash_id.size() == 0 || data._uid .size() == 0 || data._file_name.size() == 0 || data._length <= 0)
	{
		ret = -1;
	}

	//string uhash;
	data._uhash = data._uid + data._hash_id;
	file_info* f_info;

	//如果解析参数错误，直接打包，回应错误。所有参数正确时才进行check_uhash
	if ( ret == 0)
	{
		ret = check_uhash(data,f_info);
	}
	ppack(ret,data,callback,f_info,resp);

	return ret;
	
}

int video_prog_new::ppack(int ret,meta_data& data,string callback,file_info*& f_info,string& resp)
{
	string protocol = cmd_http_prog;
	
	string status = sresult_err;
	int tres = 0;
	if ( ret != 0)//ret 为0、-2时，表示正常开始
	{
		if ( ret == -2)
		{
			if ( f_info->file_end() == 0)
			{
				string resp2server;
				status = sresult_ok;
				taskid_mgr::instance()->get_taskid(data._uid, data._hash_id, data._task_id);
				pack(cmd_upload_finish,data,status,resp2server);
				msg_cmd_base *pcmd = new msg_cmd_base(1,send_upload_finish,data._uhash,resp2server);
				msg_manager::instance()->dispatch(pcmd);
			}

			pack(iret_reupload_err,data,protocol,callback,resp);
			tres = iret_reupload_err;

			return ret;
		}
		else
		{
			pack(iret_miss_para,data,protocol,callback,resp);
			tres = iret_miss_para;
		}
	}
	else
	{
		pack(iret_ok,data,protocol,callback,resp);
		tres = iret_ok;
		status = sresult_ok;
	}

	//if ( (ret == 0 || ret == -2 ) && !_send_msg)
	if ( tres == iret_ok )
	{
		string resp2server;
		pack(cmd_upload_start,data,status,resp2server);

		msg_cmd_base *pcmd = new msg_cmd_base(1,send_upload_begin,data._uhash,resp2server);
		msg_manager::instance()->dispatch(pcmd);
	}
	
	return ret;
}

int video_prog_new::check_uhash( meta_data& md, file_info*& f_info)
{
	//如果返回0，就表示该uhash曾经上传过，是否上传完成，下面再判断
	int ret = -1;
	ret = tigress_leader::get_instance()->query_info(md._uhash, f_info);
	if (ret == -1)
	{
		taskid_mgr::instance()->get_taskid(md._uid, md._hash_id, md._task_id);
		if (0 != tigress_leader::get_instance()->get_new_fileinfo(md, f_info))
		{
			//resp = "can not accept the file,maybe it is too large";
			return -1;
		}
		f_info->_meta = md;
	}
	else
	{
		md = f_info->_meta;
	}
	string tres;//no use
	//file_ready返回不为0就是没传完，只有两种选择，传完0，未传完其他
	if (0 != f_info->file_ready(tres))
	{
		/*
		if ( f_info->file_end() == 0)
		{
			string resp2server;
			string status = sresult_ok;
			pack(cmd_upload_finish,f_info->_meta,status,resp2server);
			msg_cmd_base *pcmd  = new msg_cmd_base(1,send_upload_finish,f_info->_meta._uhash,resp2server);
			msg_manager::instance()->dispatch(pcmd);
		}
		*/
		return -2;
	}
	
	f_info->_block_size = 1024*256;
	f_info->_current_block = (f_info->_meta._sha_offset) / f_info->_block_size;
	f_info->_current_len = 0;//f_info->_meta._offset % f_info->_block_size;
	f_info->_meta._offset = f_info->_meta._offset;
	f_info->_sync_offset = f_info->_meta._offset;
	f_info->_sha.Reset();

	md = f_info->_meta;

	f_info->flush_meta();

	return 0;
}

