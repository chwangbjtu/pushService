
#include <sstream>
#include <algorithm>
#include <cctype>
#include "video_upload_xml.h"
#include "tigress_leader.h"
#include "tigress_logger.h"
#include "tigress_conf.h"
#include "json.h"
#include "file_info.h"
#include "k_str.h"
#include "http_response.h"

video_upload_xml::video_upload_xml():i_accept_worker(), _body_len(0), _recv_len(0), _pv(NULL), _has_resp(PROCESSING)
{

}

video_upload_xml::~video_upload_xml()
{

}

video_upload_xml::video_upload_xml(const video_upload_xml& vu):i_accept_worker(vu)
{
	this->_body_len = vu._body_len;
	this->_recv_len = vu._recv_len;
	this->_pv = vu._pv;
	this->_has_resp = vu._has_resp;
}

i_accept_worker* video_upload_xml::get_clone()
{
	return new video_upload_xml(*this);
}

int video_upload_xml::process_header(request_t& http_req, char*& precv, long long& len, string& resp) //, void*& pv)
{
	process_response(resp);
	return -1;
}

int video_upload_xml::process_header(request_t& http_req, string& tid,string& resp)
{
        process_response(resp);
        return -1; 
}

int video_upload_xml::process_body(request_t& http_req, char* precv, long long len, string& resp)
{
	process_response(resp);
	return -1;
}

int video_upload_xml::process_body(char const * const precv,long long len,string &task_id, string& resp)
{
	process_response(resp);
	return -1;
}

int video_upload_xml::process_disconnect(request_t& header, string& reason) //, void* pinfo)
{
	return 0;
}

int video_upload_xml::process_response(string& resp)
{
	int ret = -1;

	if (_has_resp == PROCESSING)
	{
		fs::http_response http_resp;
		fs::response_t resp_t;

		string str = "keep-alive";
		resp_t.add_message_header("connection", str);
		str = "*";
		resp_t.add_message_header("Access-Control-Allow-Origin", str);
		str = "text/plain;charset=utf-8";
		resp_t.add_message_header("Content-Type", str);
		str = "GET,POST,OPTIONS";
		resp_t.add_message_header("Access-Control-Allow-Methods", str);
		str = "Content-Range";
		resp_t.add_message_header("Access-Control-Allow-Headers", str);
		str = "Content-Length";
		resp_t.add_message_header("Access-Control-Expose-Headers", str);
		
		resp_t._content = tigress_conf::get_instance()->get_xml_data();
		
		if (-1 == http_resp.pack(resp_t, resp))
		{
			resp = "";
		}
		ret = 0;
		_has_resp = HAS_RESPONSE;
	}
	else if ( _has_resp == HAS_RESPONSE)
	{
		resp = "";
		ret = 0;
	}

	return ret;
}



