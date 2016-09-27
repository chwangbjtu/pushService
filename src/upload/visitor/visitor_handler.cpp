#include "json.h"
#include "tigress_leader.h"

#include "info_leader.h"
//#include "video_get_leader.h"
//#include "video_post_leader.h"
#include "file_info.h"
#include "sync_leader.h"
#include "meta_data.h"
#include "mgmt_leader.h"


#include "file_info.h"
#include "msg_cmd_base.h"
#include "msg_manager.h"
#include "tigress_logger.h"
#include "visitor_handler.h"

#define ILLEGAL1() do{\
		char s[40] = {0};\
		in_addr addr;\
		addr.s_addr = ntohl(peer_ip());\
		char* s1 = inet_ntoa(addr);\
		strcpy(s, (const char*)s1);\
		KERROR("an illegal http packets from %s", s)\
	}while(0)

visitor_handler::visitor_handler()
{
	_ret = -1;
	_send_pos = 0;
	_msg_length = 0;
	_pcmd = NULL;
	_header_length = 0;
	_find_header = NO_HEADER;
	set_timeout(120);
	_retry_num = 100;
}

visitor_handler::~visitor_handler()
{
	

}

int visitor_handler::handle_open(void *arg)
{
	_pcmd = (msg_cmd_base*)arg;
	_req = _pcmd->get_msg();
	tigress_conf::get_instance()->get_integer_value("visitor", "retry_num", _retry_num);
	if ( _retry_num <= 0)
	{
		_retry_num = 100;
	}
	set_timeout(20);

	return 0;
}

int visitor_handler::handle_send(void) // whether to return -1
{
	ssize_t ret=0;

	if (_send_pos >= _req.size())
	{
		return 0;
	}

	while ((ret = send(_req.c_str() + _send_pos, _req.size() - _send_pos, 0) ) > 0)
	{
		_send_pos += ret;
		if (_send_pos >= _req.size())
		{
			break;
		}
	}
	if ((ret < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || ret == 0)
	{
		return -1;
	}

	return 0;
}

int visitor_handler::handle_recv(void)
{
	char buf[1024] = {0};
	ssize_t recv_len = 0;
	string::size_type position;

	while ((recv_len = recv(buf,1024,0)) > 0)
	{
		_recv.append(buf,recv_len);
	}
	if ((recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || recv_len == 0 && _recv.empty())
	{
		return -1;
	}

	fs::http_response resp;
	fs::response_t resp_t;

	if ((position = _recv.find("\r\n\r\n")) != _recv.npos)
	{
		int res = resp.parse(_recv.data(),_recv.size(),resp_t);
		if ( res == 0)
		{//Content-Length
			multimap<string, string>::iterator iter = resp_t._map_headers.begin();
			
			iter = resp_t._map_headers.find("content-length");
			if ( iter != resp_t._map_headers.end())
			{
				int len = atoi(iter->second.data());
				if ( position + len > _recv.size())
				{
					return 0;
				}
				else
				{
					_header_length = position+4;
					_msg_length = _header_length + len;
					return process_body();
				}
			}
			else
			{
				return -1;
			}
		}
	}
	else
	{
		//MAX_HEADER_SIZE
		if ( 8192 < _recv.size())
		{
			ILLEGAL1();
			return -1;
		}
	}
	
	return 0;
}

int visitor_handler::handle_close(void)
{
	if ( _ret == 0 && _pcmd != NULL)
	{
		string taskid = _pcmd->get_taskid();
		tigress_leader::get_instance()->upload_send_state(taskid, _pcmd->get_msg_type());

		file_info* fin = NULL;
		if (0 == tigress_leader::get_instance()->query_info(taskid, fin) && fin != NULL)
		{
			tigress_leader::get_instance()->flush_meta_to_disk((void *) fin);
		}
		KINFO("%s send ok,%d",taskid.data(),_pcmd->get_msg_type());
		delete _pcmd;
		_pcmd = NULL;
	}
	else if ( _pcmd != NULL && _pcmd->get_cnt() > _retry_num)//重试
	{
		string taskid = _pcmd->get_taskid();
		KINFO("%s send error,try more than %d nums,%d",taskid.data(),_retry_num,_pcmd->get_msg_type());
		delete _pcmd;
		_pcmd = NULL;
	}

	if ( _pcmd != NULL)
	{
		string taskid = _pcmd->get_taskid();
		KINFO("%s send error,need to try again,%d",taskid.data(),_pcmd->get_msg_type());
		_pcmd->add_cnt();
		msg_manager::instance()->dispatch(_pcmd);
	}

	return -1;
}

int visitor_handler::handle_run(time_t tm)
{
	return 0;
}

int visitor_handler::parse_header(string::size_type position)
{
	return 0;
}

int visitor_handler::process_body()
{
	string s_body(_recv.data()+_header_length, _msg_length-_header_length);

	string ret,error_info;
	pandaria::json jn;
	if (!jn.parse(s_body, error_info))
	{
		KINFO("%s, response err,json can not parse",s_body.data());
		return -1;
	}
	
	ret = jn.get("ret", ret, error_info);

	if ( ret.size() == 0)
	{
		KINFO("%s, response ret is null,or ret is not find",s_body.data());
		return -1;
	}
	else
	{
		_ret = 0;
	}

	return -1;//返回-1，是为了断开连接，process_body被调用是，表示已经接受数据结束
}


