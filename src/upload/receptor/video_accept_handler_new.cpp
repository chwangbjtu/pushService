
#include <iostream>
#include <sstream>
#include "video_accept_handler_new.h"
#include "video_worker_manager.h"
#include "tigress_logger.h"
#include "tigress_conf.h"

using namespace std;

#define ILLEGAL() do{\
		char s[40] = {0};\
		in_addr addr;\
		addr.s_addr = ntohl(peer_ip());\
		char* s1 = inet_ntoa(addr);\
		strcpy(s, (const char*)s1);\
		KERROR("an illegal http packets from %s", s)\
		_disconn_reason = "illegal packets";\
	}while(0)

#define DISCONN(x) if (x == 0 || errno == ECONNRESET || errno == EPIPE)\
		{\
			_disconn_reason = "peer reset or close";\
		}\
		else\
		{\
			_disconn_reason = "unknown ";\
			_disconn_reason += strerror(errno);\
		}


video_accept_handler_new::video_accept_handler_new()
{
	_start_time = time(NULL);
	_send_pos = 0;
	_precv = NULL;

	_msg_length = 0;
	_msg_length1 = -1;
	_header_length = 0;
	_recv_length = 0;
	_data_length = 0;
	_content_length = 0;
	_table_header_length = -1;
	_ttlen = 0;
	_body_recv = 0;
	_length = 0;
	
	_find_header = NO_HEADER;
	_find_form_header = false;
	_responsed = false;
	_found_error = false;
	_upload_statuts = false;
	
	//_recv.reserve(3072);
	//_resp.reserve(3072);

	_pworker = NULL;
	_disconn_reason = "close(probably by peer)";
	if (-1 == tigress_conf::get_instance()->get_integer_value("receptor", "timeout", _service_timeout))
	{
		_service_timeout = TIME_OUT;
	}
}

video_accept_handler_new::~video_accept_handler_new()
{
	if (NULL != _pworker)
	{
		delete _pworker;
		_pworker = NULL;
	}
}

int video_accept_handler_new::reset()
{
	_start_time = time(NULL);
	_send_pos = 0;
	_precv = NULL;

	_msg_length = 0;
	_msg_length1 = -1;
	_header_length = 0;
	_recv_length = 0;
	_data_length = 0;
	_content_length = 0;
	_table_header_length = -1;
	_ttlen = 0;
	_body_recv = 0;
	_length = 0;
	
	_find_header = NO_HEADER;
	_find_form_header = false;
	_responsed = false;
	_found_error = false;
	_upload_statuts = false;

	_http_req.reset();

	return 0;

}

int video_accept_handler_new::handle_open(void* arg)
{
	_recv.reserve(1024*256);
	_resp.reserve(1024);

	return 0;
}


int video_accept_handler_new::handle_send(void)
{
	ssize_t ret=0;
	const char* pstart = _resp.data();
	unsigned int resp_len  = _resp.size();

	if (_resp.empty())
	{
		return 0;
	}

	while ( _send_pos < resp_len)
	{
		ssize_t tn = send(pstart+_send_pos,resp_len-_send_pos,0);
		if ( tn > 0)
		{
			_send_pos += (size_t)tn;
		}
		else if ( tn < 0 && (errno == EAGAIN || errno == EWOULDBLOCK))
		{
			return 0;
		}
		else 
		{
			break;
		}
	}
	_resp.clear();

	_start_time = time(NULL);

	return -1;
}


int video_accept_handler_new::handle_recv(void)
{
	char buf[2048] = {0};
	ssize_t recv_len;

	if ( _found_error)
	{
		KERROR("found_error")
		KERROR("recv size:%d,resp size:",_recv.size(),_resp.size())
		return -1;
	}

	if (_find_header == FOUND_HEADER)
	{
		if ( _find_form_header)
		{
			_recv.clear();
		}
		
		while ((recv_len = recv(buf,2048,0)) > 0)
		{
			int pos = -1;
			_recv.append(buf,recv_len);
			_recv_length += recv_len;
			
			if ( _recv.size() >= 1024*128)
			{
				_start_time = time(NULL);
				
				int begin = -1;
				bool thas_header = false;
				if ( !_find_form_header)
				{
					_table_header_length = found_form_header();
					if ( _table_header_length != -1)
						thas_header = true;
				}
				
				//写入数据
				write_data(thas_header);
			}
		}
		if (recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN)
		{
			DISCONN(recv_len);
			KERROR("recv_len < 0")
			return -1;
		}

		//未凑够128K数据就提前结束，可能数接收完了，也可能没有
		
		_start_time = time(NULL);
		if ( !_find_form_header)
		{
			_table_header_length = found_form_header();
			if ( _find_form_header)
			{
				write_data(true);
			}
		}
		else
		{
			write_data(false);
		}
	}
	else if (_find_header == NO_HEADER)
	{
		while ((recv_len = recv(buf,2048,0)) > 0)
		{
			_recv.append(buf,recv_len);
			_recv_length += recv_len;
		}
		if (recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN)
		{
			DISCONN(recv_len);
			KERROR("recv_len  < 0 and errno != EAGAIN")
			return -1;
		}
		
		_start_time = time(NULL);

		int parse_status = parse();
		if ( _upload_statuts && _length < 0)
		{
			KERROR("upload protocol not find length key")
			return -1;
		}

		if ( parse_status == 0)
		{
			if ( _method == "GET")//非上传报文
			{
				_pworker->process_header(_http_req,_taskid,_resp);
			}
			else if ( !_upload_statuts && _recv.size() >= _msg_length)//非上传报文
			{
				_pworker->process_body(_recv.data()+_header_length,_recv.size()-_header_length,_taskid,_resp);
			}
			else//上传报文
			{
				int pos = -1;
				
				pos = found_form_header();
				if ( pos != -1)
				{
					_table_header_length = pos;//pos has pass "\r\n\r\n" , no need +4
					int ret = _pworker->process_header(_http_req, _taskid,_resp);
					if ( ret != 0)
					{
						KERROR("prcess_header error")
						return ret;
					}
					//写入数据
					write_data(true);
				}
			}
		}
		else if (parse_status == -2)
		{
			return -1;
		}
		else
		{
			if (MAX_HEADER_SIZE < _recv.size())
			{
				KERROR("recv size:%d,resp size:",_recv.size(),_resp.size())
				_found_error = true;
				ILLEGAL();
				KERROR("max_head_size %d,  recv size: %d",MAX_HEADER_SIZE,_recv.size())
				return -1;
			}
		}
	}

	if ( _recv_length >= _msg_length && _msg_length > 0 && _find_form_header && _resp.size() == 0)
	{
		string uhash = _uid + _hashid;
		if ( _pworker != NULL)
		{
			_pworker->get_part_resp(uhash,_resp);
		}
	}
	if ( _resp.size() != 0)
	{   
		KERROR("recv resp not null,send")
		return handle_send();
	} 

	return 0;
	
}


int video_accept_handler_new::handle_close(void)
{
	if (NULL != _pworker)
	{
		_pworker->process_disconnect(_http_req, _disconn_reason); //?????????????????
		delete _pworker;
		_pworker = NULL;
	}

	return 0;
}


int video_accept_handler_new::handle_run(time_t tm)
{
	if (tm - _start_time  > _service_timeout)
	{
		_disconn_reason = "local timeout";
		KERROR("timeout")
		return -1;
	}

	return 0;
}

int video_accept_handler_new::parse_header(string::size_type position)
{
	unsigned char* recv_p = (unsigned char*)(_recv.data());
	_header_length = position;//include the \r\n\r\n

	if ( _recv.size() > 10)
	{
		string tmp = _recv.substr(0,10);
		if ( tmp.find("GET") == -1 && tmp.find("POST") == -1 && tmp.find("OPTIONS") == -1)
		{
			KERROR("not find header :%s" , tmp.data())
			return -1;
		}
	}

	fs::http_request req;

	if (0 != req.parse((char*)recv_p, _header_length, _http_req)) //parse the http header
	{
		return -1;
	}
	
	string str =  _http_req.get_content_length();
	long long gcl = 0;
	if (!str.empty())
	{
		gcl = atoll(str.c_str());
	}
	_content_length = gcl;
	_msg_length = _header_length + gcl;
	_find_header = FOUND_HEADER;
		
	_path = _http_req.get_url();
	_method = _http_req._method;

	_http_req.get_param("uid", _uid);
	_http_req.get_param("hashid",_hashid);
	_taskid = _uid + _hashid;
	
	//if (_uid.size() == 0 || _hashid.size() ==0)
	//{
	//	KERROR("uid or hashid is null,uid :%s,hashid :%s",_uid.data(),_hashid.data())
	//	return -2;
	//}
	string tstr;
	_http_req.get_param("length", tstr);
	if (!tstr.empty())
	{
		_length = atoll(tstr.c_str());
	}
	

	multimap<string, string>::iterator iter = _http_req._map_headers.find("content-type");
	if ( iter != _http_req._map_headers.end() && _boundary_str.size() == 0)
	{
		int index = -1;
		index = iter->second.find("boundary=");
                
		if ( index != -1 && index + 9 <= iter->second.size())
		{
			int tindex = iter->second.find("\r\n");
			if ( tindex != -1 && tindex > index +9)
				_boundary_str = "--" + iter->second.substr(index +9,iter->second.size()-2);
			else
				_boundary_str = "--" + iter->second.substr(index +9);
			
		}
	}

	if ( _path == "/tigress/upload" && _method == "POST")
	{
		_upload_statuts = true;
		if ( _length <= 0)
		{
			return -2;//pase_error
		}
	}

	return 0;
}

int video_accept_handler_new::process_header()
{
	return 0;

}

int video_accept_handler_new::parse()
{
	int res = -1;
	int position = -1;
	position = _recv.find("\r\n\r\n");
	if ( position  != -1)
	{
		if (0 == parse_header(position + 4))
		{
			int ret = ( static_cast<video_worker_manager*>(userarg()) )->get_accept_worker(_http_req, _pworker);
			if (0 != ret)
			{
				KERROR("cannot find worker,recv size: %d",_recv.size())
				res = -1;
			}
			else
			{
				res = 0;
			}
		}
		else
		{
			res = -2;
			return res;
		}
	}
	return res;
}

bool video_accept_handler_new::check_msg_boundary(int start,int & pos)
{
	bool res = false;
	if (_boundary_str.size() != 0)
	{
		pos = -1;
		pos = _recv.find(_boundary_str,start);
		if (pos >0 && pos != std::string::npos)
        	{
                	res = true;
        	}
	}
	return res;
}


int video_accept_handler_new::found_form_header()
{
	int form_pos = -1;
	int tmp = -1;

	if (check_msg_boundary(0,tmp) && tmp != -1 )//必须能找到"boundary"表单开始标志
	{
		int pos = _recv.find("Content-Disposition",tmp);
		int resource_pos = -1;//_recv.find("name=\"resource\"");
		int end_pos = -1;//
		if ( pos != -1)
		{
			resource_pos = _recv.find("name=\"resource\"",pos);
			if ( resource_pos != -1)
			{
				end_pos = _recv.find("\r\n\r\n",resource_pos);
				if ( end_pos != -1)
				{
					form_pos = end_pos+4;
					_find_form_header = true;
				}
			}
		}
	}

	return form_pos;
}

int video_accept_handler_new::write_data(bool has_header)
{
	bool has_tail = check_has_tail();
	const char* data_pos = NULL;
	int data_len = 0;
	int res = -1;
	res = get_data_pos(has_header,has_tail,data_pos,data_len);
	if ( res != -1 && data_pos != NULL && data_len > 0)
	{
		if ( _pworker != NULL)
		{
			_pworker->process_body(data_pos,data_len,_taskid,_resp);
			_recv.clear();
		}
	}
	return 0;
}

bool video_accept_handler_new::check_has_tail()
{
	bool has_tail = false;
	int trecv_len = _recv_length - _recv.size();
	if ( trecv_len < _table_header_length + _length && _recv_length > _table_header_length + _length)
	{
		has_tail = true;
	}

	return has_tail;
}

int video_accept_handler_new::get_data_pos(bool has_header,bool has_tail,const char*& cpos,int& data_len)
{
	int trecv_len = _recv_length - _recv.size();
	//视频数据早已接收完，之后的都是无用数据直接抛弃
	if ( trecv_len >= (_table_header_length + _length))
	{
		return -1;
	}

	if ( has_header && has_tail)
	{
		cpos = _recv.data() + _table_header_length;
		data_len = _length;
	}
	else if ( has_header && ! has_tail)
	{
		cpos = _recv.data() + _table_header_length;
		data_len = _recv.size() - _table_header_length;
	}
	else if ( !has_header && has_tail)
	{
		cpos = _recv.data();
		data_len = _table_header_length + _length - trecv_len;
	}
	else
	{
		cpos = _recv.data();
		data_len = _recv.size();
	}

	return 0;
}


