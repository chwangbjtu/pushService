
#include <sstream>
#include <algorithm>
#include <cctype>
#include "ret_code.h"
#include "video_upload_new.h"
#include "tigress_leader.h"
#include "tigress_logger.h"
#include "json.h"
//#include "file_info.h"
#include "k_str.h"
#include "http_response.h"

#include "tigress_conf.h"
#include "msg_cmd_base.h"
#include "msg_manager.h"


video_upload_new::video_upload_new():i_accept_worker()
{
}

video_upload_new::~video_upload_new()
{

}

video_upload_new::video_upload_new(const video_upload_new& vu):i_accept_worker(vu)
{
}

i_accept_worker* video_upload_new::get_clone()
{
	return new video_upload_new(*this);
}

int video_upload_new::process_header(request_t& http_req, char*& precv, long long& len, long long& data_len,string& resp)
{
	string uhash;
	int ret = process_header(http_req,precv,len,data_len,resp,uhash);

	if (ret != 0 && uhash.size() != 0)
	{
		file_info * pv = NULL;
		tigress_leader::get_instance()->query_info(uhash, pv);
		if ( pv != NULL)
		{
			string resp2server;
			pack(cmd_upload_finish,pv->_meta,sresult_err,resp2server);
			msg_cmd_base *pcmd = new msg_cmd_base(1,send_upload_finish,uhash,resp2server);
			msg_manager::instance()->dispatch(pcmd);
		}
	}

	return ret;
}

int video_upload_new::parse_param(request_t& http_req,meta_data& data,file_info*& fin,string& resp)
{
	if (0 != http_req.get_param("fileid", data._file_id))
	{
		//return -1;
	}

	if (0 != http_req.get_param("uid", data._uid))
	{
		pack(iret_miss_para,data,"","",resp);
		return -1;
	}

	if (0 != http_req.get_param("hashid", data._hash_id))
	{
		pack(iret_miss_para,data,"","",resp);
		return -1;
	}

	string off;
	if (0 != http_req.get_param("offset", off))
	{
		pack(iret_miss_para,data,"","",resp);
		return -1;
	}
	long long oft = atoll(off.c_str());
	data._offset = oft;

	string checksum;
	if ( 0!= http_req.get_param("c",checksum))
	{
		pack(iret_miss_para,data,"","",resp);
		return -1;
	}

	data._uhash = data._uid + data._hash_id;
	
	if ( off.empty() || 0 != tigress_leader::get_instance()->query_info(data._uhash, fin))//没检查是否接收完，就直接返回fin指针
	{
		pack(iret_para_err,data,"","",resp);
		return -1;
	}

	if ( fin->file_recv_over())
	{
		return -1;
	}
	
	if ( oft > fin->_meta._offset)
	{
		KERROR("an illegal http packet for file %s with wrong offset %lld should be %lld ", data._uhash.c_str(), oft, fin->_meta._sha_offset)
		pack(iret_para_err,data,"","",resp);
		return -1;
	}
	else if (oft < fin->_meta._offset)
	{
		KWARN("an illegal http packet for file %s with wrong offset %lld should be %lld ", data._uhash.c_str(), oft, fin->_meta._sha_offset)
	}

	fin->_meta._offset = oft;
	fin->_meta._sha_offset = oft;
	
	return 0;
}

int video_upload_new::process_header(request_t& http_req, char*& precv, long long& len, long long& data_len,string& uhash,string& resp) //, void*& pv)
{
	//string off, fid, taskid,uid,hashid,err,checksum;
	file_info* fin;

	meta_data data;
	int res = parse_param(http_req,data,fin,resp);
	if ( res != 0)
	{
		return res;
	}

	uhash = data._uhash;
	
	precv = fin->_mmp_start + data._offset;
	//string str = http_req.get_content_length();
	data_len = fin->_meta._length-data._offset;

	return 0;
}

int video_upload_new::process_header(request_t& http_req, string& uhash,string& resp)
{
	//string off, fid, taskid,uid,hashid,err,checksum;
	file_info* fin;
	meta_data data;
	int res = parse_param(http_req,data,fin,resp);
	if ( res != 0)
	{
		return res;
	}

	uhash = data._uhash;

	return 0;
}
int video_upload_new::process_body(request_t& http_req, char* precv, long long len, string& resp)
{
	return 0;
}

int video_upload_new::process_body(char const * const precv,long long len,string &uhash, string& resp)
{
	file_info  *f_info;

	int ret = tigress_leader::get_instance()->query_info(uhash, f_info);
	if (ret == -1)
	{
		return -1;
	}

	//memmove(_precv, recv_p + _table_header_length, rest_len - _table_header_length);
	long long data_len = f_info->_meta._length - f_info->_meta._offset;
	long long reset_len = (data_len > len )? len:data_len;
	if ( reset_len > 0)
	{
		memmove(f_info->_mmp_start + f_info->_meta._offset,precv,reset_len);

		char * pinfo = (char*)(f_info->_mmp_start + f_info->_meta._offset);
		if ( 0 != f_info->file_update(pinfo, reset_len))
		{	
			KERROR("the file %s process body fail", f_info->_meta._uhash.c_str())
			return -1;
		}
	}
	
	int ret1 = f_info->file_end();
	if ( 0 == ret1)
	{
		meta_data data;
		data = f_info->_meta;
		pack(iret_ok,data,"","",resp);//protocal为空是为了不返回key字段

		string resp2server;
		pack(cmd_upload_finish,data,sresult_ok,resp2server);

		msg_cmd_base *pcmd = new msg_cmd_base(1,send_upload_finish,data._uhash,resp2server);
		msg_manager::instance()->dispatch(pcmd);

		f_info->flush_meta();
	}
	
	return 0;
}

int video_upload_new::get_part_resp(string& uhash,string& resp)
{
	file_info  *f_info;

	int ret = tigress_leader::get_instance()->query_info(uhash, f_info);
	if (ret == -1)
	{
		return -1;
	}

	meta_data data;
	data = f_info->_meta;
	pack(iret_ok,data,"","",resp);//protocal为空是为了不返回key字段

	return 0;
}

int video_upload_new::process_disconnect(request_t& header, string& reason)
{
	string uid;
	string hashid;
	string uhash;
	if (0 != header.get_param("uid", uid))
	{
		return -1;
	}

	if (0 != header.get_param("hashid", hashid))
	{
		return -1;
	}

	uhash = uid + hashid;

	file_info  *f_info;

	int ret = tigress_leader::get_instance()->query_info(uhash, f_info);
	if (ret == -1)
	{
		return -1;
	}

	if (f_info != NULL)
	{
		int ret = f_info->file_end();
		if ( ret != 0)
		{
			string uhash = f_info->_meta._uhash;
			string resp2server;
			pack(cmd_upload_finish,f_info->_meta,sresult_err,resp2server);
			msg_cmd_base *pcmd = new msg_cmd_base(1,send_upload_finish,uhash,resp2server);
			msg_manager::instance()->dispatch(pcmd);
		}
	}
	
	return 0;
}

int video_upload_new::process_response(string& resp)
{
	return 0;
}


