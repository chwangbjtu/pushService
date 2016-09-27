#include "i_accept_worker.h"

#include <sstream>
//#include <algorithm>
//#include <cctype>
#include "ret_code.h"
//#include "video_upload.h"
//#include "tigress_leader.h"
//#include "tigress_logger.h"
#include "tigress_conf.h"
#include "json.h"
#include "file_info.h"
#include "md5_mgr.h"
//#include "k_str.h"
#include "http_request.h"
#include "http_response.h"

//返回给上传视频的客户端,对第一、二个报文回应
int i_accept_worker::pack(const int status,meta_data& data,const string protocal,string callback,string& resp)
{
	pandaria::json jn;
	stringstream st;
	string tmp;
	string sret = "ret";
	string sres = "";
	if ( iret_ok == status)
		sres = sret_ok;
		//jn.add(sret,sret_ok);
	else if ( iret_miss_para == status)
		sres = sret_miss_para;
		//jn.add("ret",sret_miss_para);
	else if ( iret_para_err== status)
		sres = sret_para_err;
		//jn.add("ret",sret_para_err);
	else if ( iret_para_timeout == status)
		sres = sret_para_timeout;
		//jn.add("ret",sret_para_timeout);
	else if ( iret_reupload_err == status)
		sres = sret_reupload_err;
		//jn.add("ret",sret_reupload_err);
	else
		sres = sret_server_err;
		//jn.add("ret",sret_server_err);

	jn.add(sret,sres);
	//if ( tpf != NULL)
	{
		//file_info* pf = static_cast<file_info*>(tpf);
		if ( !data._file_id.empty())
		{
			jn.add("fileid",data._file_id);
		}
		if ( !data._task_id.empty())
		{
			jn.add("taskid",data._task_id);
		}
		st<<data._offset;
		st>>tmp;
		jn.add("offset", tmp);

		//if ( protocal == "prog")
		if ( protocal == cmd_http_prog)
		{
			jn.add("key",data._key);
		}
		
	}

	string str = "close";
	/*
	if ( iret_ok == status)
	{
		str = "keep-alive";
	}
	*/

	tmp = jn.to_formated_str();
	
	fs::http_response http_resp;
	fs::response_t resp_t;
	

	resp_t.add_message_header("connection", str);
	str = "*";
	resp_t.add_message_header("Access-Control-Allow-Origin", str);
	str = "text/plain;charset=utf-8";
	resp_t.add_message_header("Content-Type", str);
	str = "GET,POST,OPTIONS";
	resp_t.add_message_header("Access-Control-Allow-Methods", str);
	str = "Content-Length";
	resp_t.add_message_header("Access-Control-Expose-Headers", str);

	if ( callback.size() != 0)
	{
		resp_t._content = callback + "(" + tmp + ")";
	}
	else
	{
		resp_t._content = tmp;
	}
	
	if (-1 == http_resp.pack(resp_t, resp))
	{
		resp = "";
	}

	return 0;
}

//打包给maze的报文
int i_accept_worker::pack(const string type,meta_data& data,string status,string& resp)
{
	pandaria::json jn;
	stringstream st;
	string tmp;

	jn.add("task_id",data._task_id);
	jn.add("uid",data._uid);
	jn.add("hashid",data._hash_id);
	tigress_conf::get_instance()->get_string_value("info_manager", "file_paths", tmp);
	tmp = tmp + data._uhash + ".down";
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
	url = url + data._uhash + ".down" + "#md5=" + md5str;
	jn.add("file_url",url);

	string str = "close";
	//string str = "keep-alive";

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
		jn.add("result",status);
	}
	else if ( type == cmd_transcode_add)
	{
		req_t._path = cmd_transcode_add_path;
	}
	req_t.add_message_header("connection", str);
	str = "text/plain;charset=UTF-8";
	req_t.add_message_header("Content-Type", str);

	//Content-Length 会在pack时自动添加
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

