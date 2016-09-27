
#include <iostream>
#include <sstream>
#include "video_accept_handler.h"
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


video_accept_handler::video_accept_handler()
{
	_send_pos = 0;
	_start_time = time(NULL);
	_precv = NULL;

	_find_header = NO_HEADER;
	_table_header_length = -1;
	_msg_length = 0;
	_msg_length1 = -1;
	_ttlen = 0;
	_header_length = 0;
	_recv_length = 0;
	_data_length = 0;
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

video_accept_handler::~video_accept_handler()
{
	if (NULL != _pworker)
	{
		delete _pworker;
		_pworker = NULL;
	}
}

int video_accept_handler::reset()
{
	_send_pos = 0;
	_start_time = time(NULL);
	_recv.clear();
	_resp.clear();
	_find_header = NO_HEADER;

	_msg_length = 0;
	_table_header_length = -1;
	_msg_length1 = -1;
	_ttlen = 0;
	_header_length = 0;
	_recv_length = 0;
	_data_length = 0;
	_responsed = false;

	_http_req.reset();

	return 0;

}

int video_accept_handler::handle_open(void* arg)
{
	_recv.reserve(1024*256);
	_resp.reserve(1024);

	return 0;
}


int video_accept_handler::handle_send(void)
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


int video_accept_handler::handle_recv(void)
{
	char buf[1024] = {0};
	ssize_t recv_len;
	string::size_type position;

	if ( _found_error)
	{
		return -1;
	}

	if (_find_header == FOUND_HEADER)
	{
		char* ptr = _precv;
		ssize_t t_len = 0;
		ssize_t rest_body_len = 0;

		//ssize_t rest_body_len = _msg_length - _recv_length;
		//ssize_t rest_body_len = _msg_length - _table_header_length;
		//if ( _path == "/tigress/upload")
		if ( _upload_statuts)
		{
			rest_body_len = _msg_length1 - _recv_length;
		}
		else
		{
			rest_body_len = _msg_length - _recv_length;
		}
		ssize_t rest_recv_len = (rest_body_len > 1024*32) ? 1024*32 : rest_body_len;
		//if ( _path != "/tigress/upload" )
		if ( !_upload_statuts)
		{
			rest_recv_len = (rest_recv_len > 0) ? rest_recv_len : 1;
		}
		while ( rest_recv_len > 0 && (recv_len = recv(_precv, rest_recv_len, 0)) > 0)//
		{
			_precv += recv_len;
			t_len += recv_len;
			rest_body_len -= recv_len;
			rest_recv_len = (rest_body_len > 1024*32) ? 1024*32 : rest_body_len;

			_ttlen += recv_len;


			//if ( _path == "/tigress/upload" && rest_recv_len <= 0)
			if ( _upload_statuts && rest_recv_len <= 0)
			{
				break;
			}
			else
			{
				rest_recv_len = (rest_recv_len > 0) ? rest_recv_len : 1;
			}
		}

		//if ( rest_recv_len <= 0 && recv_len>0 && _path == "/tigress/upload")
		if ( rest_recv_len <= 0 && recv_len>0 && _upload_statuts)
		{
			while ((recv_len = recv(buf,1024,0)) > 0)
                	{	   
				_recv.append(buf,recv_len);
                	} 
		}
		
		if ((recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || recv_len == 0)
		{
			DISCONN(recv_len);
			//stringstream str;
			//str<<(long long)_precv;
			//_disconn_reason += "addr now:";
			//_disconn_reason += str.str();
			return -1;
		}

		_start_time = time(NULL);
		_recv_length += t_len;
		//只是为了把sha_offset增加t_len长度，并且把刚刚写入内存映射的数据，写入磁盘
		int ret = -1;
		//if ( _path == "/tigress/upload" && _msg_length1 < _recv_length)
		{
			;
		}
		ret = _pworker->process_body(_http_req, ptr, t_len, _resp);

		if ( _resp.empty())
		{
			_pworker->process_response(_resp);
		}
		
		if (!_resp.empty()) 
		{
			//_found_error = true;
			handle_send();
			return -1;
		}
		
		return ret;
	}
	else if (_find_header == NO_HEADER)
	{
		while ((recv_len = recv(buf,1024,0)) > 0)
		{
			_recv.append(buf,recv_len);
		}
		if ((recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || recv_len == 0)
		{
			DISCONN(recv_len);
			//stringstream str;
			//str<<(long long)_precv;
			//_disconn_reason += " addr now:";
			//_disconn_reason += str.str();
			return -1;
		}
		_start_time = time(NULL);
		_recv_length = _recv.size();

		if ((position = _recv.find("\r\n\r\n")) != _recv.npos)
		{
			if (0 == parse_header(position + 4) && 0 == process_header())
			{
				return 0;
			}
			else
			{
				if ( !_resp.empty())
				{
					_found_error = true;
					handle_send();
				}
				//ILLEGAL();
				return -1;
			}
		}
		else
		{
			if (MAX_HEADER_SIZE < _recv.size())
			{
				_found_error = true;
				ILLEGAL();
				return -1;
			}
		}
	}

	return 0;
	
}


int video_accept_handler::handle_close(void)
{
	if (NULL != _pworker)
	{
		_pworker->process_disconnect(_http_req, _disconn_reason); //?????????????????
		delete _pworker;
		_pworker = NULL;
	}

	return 0;
}


int video_accept_handler::handle_run(time_t tm)
{
	/*
	if (_pworker != NULL && 0 == _pworker->process_response(_resp))
	{
		 if (!_resp.empty())
			 handle_send();
	}*/
	if (tm - _start_time  > _service_timeout)
	{
		_disconn_reason = "local timeout";
		return -1;
	}

	return 0;
}

int video_accept_handler::parse_header(string::size_type position)
{
	unsigned char* recv_p = (unsigned char*)(_recv.data());
	_header_length = position;//include the \r\n\r\n
	int ret = -1;
	fs::http_request req;

	if (0 == req.parse((char*)recv_p, _header_length, _http_req)) //parse the http header
	{
		string str =  _http_req.get_content_length();
		long long gcl = 0;
		if (!str.empty())
		{
			gcl = atoll(str.c_str());
			//_data_length = gcl;
		}
		
		_msg_length = _header_length + gcl;
		_find_header = FOUND_HEADER;
		ret = 0;
	}
	_path = _http_req.get_url();
	_method = _http_req._method;

	if ( _path == "/tigress/upload" && _method == "POST")
	{
		_upload_statuts = true;
	}

	return ret;
}

int video_accept_handler::process_header()
{
	int ret = -1;

	i_accept_worker* a_worker = NULL;
	ret = ( static_cast<video_worker_manager*>(userarg()) )->get_accept_worker(_http_req, a_worker);
	if (0 != ret)
	{
		return -1;
	}

	//if ( _path == "/tigress/upload")
	if ( _upload_statuts)
	{
		ret = a_worker->process_header(_http_req, _precv, _recv_length,_data_length, _resp);
	}
	else
	{
		ret = a_worker->process_header(_http_req, _precv, _recv_length, _resp);
	}

	if (0 != ret)
	{
		return -1;
	}
	
	if (_pworker != NULL)
		delete _pworker;
	_pworker = a_worker;

	unsigned char* recv_p = (unsigned char*)(_recv.data());
	ssize_t rest_len = (_recv.size() >= _msg_length) ? _msg_length : _recv.size();

	//_path = _http_req.get_url();
	//if ( _path == "/tigress/upload")
	if ( _upload_statuts)
	{
		_table_header_length = _recv.find("\r\n\r\n",_header_length);
		if ( _table_header_length != -1 && _table_header_length <= _recv.size() && rest_len - (_table_header_length+4) > 0)
		{
			_table_header_length += 4;
			memmove(_precv, recv_p + _table_header_length, rest_len - _table_header_length);
			
			_ttlen = _ttlen + (rest_len - _table_header_length);
			
			_msg_length1 = _table_header_length  + _data_length;
			if ( _msg_length1 <= 0 || _msg_length1 == -1)
			{
				return -1;
			}
		}

	}
	else
	{
		memmove(_precv, recv_p + _header_length, rest_len - _header_length);
	}
	
	//memmove(_precv, recv_p + _header_length, rest_len - _header_length);
	
	//if ( _path == "/tigress/upload")
	if ( _upload_statuts)
	{
		ret = _pworker->process_body(_http_req, _precv, rest_len - _table_header_length, _resp);
		_precv += (rest_len - _table_header_length);
	}
	else
	{
		ret = _pworker->process_body(_http_req, _precv, _recv.size() - _header_length, _resp);
		_precv += (_recv.size() - _header_length);
	}
	//_precv += (_recv.size() - _header_length);

	if ( _resp.empty())
	{
		_pworker->process_response(_resp);
	}

	//if (_resp.size() != 0)
	//{
	//	return handle_send();
	//}
	

	return ret;

}


