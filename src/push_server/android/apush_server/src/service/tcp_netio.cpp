#include <sys/time.h>
#include <sstream>
#include "tcp_netio.h"
#include "dbg.h"
#include "en_interface.h"
#include "user_mgr.h"
#include "msg_mgr.h"
#include "configure.h"
#include "proto_process.h"
#include "proto_dispatcher.h"
#include "proto_constant.h"
#include "proto_struct.h"

#include "tlogger.h"
#include "util.h"


using namespace std;

tcp_netio::tcp_netio():
	_send_len(0)
{
    _ctime = time(NULL);
	_service_timeout = configure::instance()->get_service_timeout();
    _id = -1;
}

tcp_netio::~tcp_netio()
{
}
int tcp_netio::handle_recv()
{
	const int BUF_LEN = 512;
	char buf[BUF_LEN] = {0};
	ssize_t recv_len = 0;
	while((recv_len = ::recv(sock(), buf, BUF_LEN, 0)) > 0) 
	{
		_request.append(buf, recv_len);
        if (_request.size() > max_recv_packet)
        {
            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: %s", util::get_conn_id(_thread_index, _id), _token.c_str(), "packet too long");
            tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,1,1);
            return -1;
        }
	}
	if(recv_len < 0 && (errno != EAGAIN && errno != EWOULDBLOCK)) 
	{
        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: %s, errno: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), "caused by recv error", errno);
        tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,2,1);
		return -1;
	} 
	else if(recv_len == 0) 
	{
        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: %s", util::get_conn_id(_thread_index, _id), _token.c_str(), "client close");
        tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,3,1);
		return -1;
	}
    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: get packet, req buffer: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), _request.size());

	int length = 0;
	if ( _request.size() >= proto_header_len)
	{
    	//length = get_length();
    	length = ftsps::getlen((unsigned char*)_request.c_str());
	}

	if (length < 0 || length > max_recv_packet)
	{
        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: req buffer length < proto_header_len", util::get_conn_id(_thread_index, _id), _token.c_str());
        tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,4,length);
		return -1;
	}

	_ctime = time(NULL);


    //客户端可能一次发送多个数据包过来,需要一次处理多个数据包
    int res = 0;
    //while (_request.size() > 0 && _request.size() >= length + sizeof(header_struct_t) && res == 0 && length <= max_recv_packet)
    //while (_request.size() >= length + proto_header_len && res == 0)
    while (_request.size() >= length && res == 0 && length > 0)
    {
        ///*
        int tres = 0;
        tres = ftsps::decrypt((unsigned char*)_request.c_str(),length);
        //if ( ftsps::decrypt((unsigned char*)_request.c_str(),length) < 0)
        if ( res < 0)
        {
            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: %s, errno: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), "decrypt packet error", tres);
            tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,5,1);
            return -1;
        }
        //*/

        string tresp;
        string rtoken;
        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: process packet", util::get_conn_id(_thread_index, _id), _token.c_str());
        res = proto_dispatcher::instance()->process(_request, peer_ip(),_thread_index,_id,_token,tresp);
        //if ( _token.size() == 0 && rtoken.size() > 0)
        //{
        //    _token = rtoken;
        //}
        //
        ///*
        if ( tresp.size() > 0 && ftsps::encrypt((unsigned char*)tresp.data(),tresp.length()) < 0)
        {
            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: %s", util::get_conn_id(_thread_index, _id), _token.c_str(), "encrypt response packet error");
            tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,100,0);
            return -1;
        }
        //*/
        if ( res == 0)
        {
            _response.append(tresp);
        }

		length = 0;
		if ( _request.size() >= proto_header_len)
		{
    	    //length = get_length();
			length = ftsps::getlen((unsigned char*)_request.c_str());;
			if ( length > max_recv_packet)
			{
                tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: %s", util::get_conn_id(_thread_index, _id), _token.c_str(), "unknown");
                tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,6,1);
				return -1;
			}
		}

		if ( res != 0)
        {
            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: close, reason: %s, errno: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), "process packet error", res);
            tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,7,1);
			return -1;
        }
	}
    //if(proto_dispatcher::instance()->process(_request, peer_ip(),_thread_index,_id,_response) < 0)
    if (res < 0)
    {
        tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,8,1);
        return -1;//close socket
    }
    else
    {
        return handle_send();
    }

    return 0;
}

int tcp_netio::handle_open(void *arg)
{
    _id = user_mgr::instance()->get_uid(_thread_index);
    if ( _id < 0)
    {
        //DBG_ERROR("get uid error,%d,%d",_thread_index,_id);
        return -1;
    }
    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: connection open", util::get_conn_id(_thread_index, _id), _token.c_str());
	return 0;
}

int tcp_netio::handle_send()
{
	if(_response.length() == 0) 
	{
		return 0;
	}
	size_t resp_len = _response.length();
    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: send, length: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), resp_len);
	while (_send_len < resp_len) 
	{
		ssize_t n = ::send(sock(), _response.data()+_send_len,resp_len-_send_len, 0);
		if(n > 0)
		{
			_send_len += (size_t)n;
		}
		else if(n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK ))
		{
			/* action blocked */
            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: send partial, length: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), _send_len);
			return 0;
		}
		else 
		{
            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: send finish, errno: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), errno);
			break;
		}
	}
	//send all response
	_response.clear();
    _send_len = 0;

    return 0;
}
int tcp_netio::handle_close()
{
    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: connection close", util::get_conn_id(_thread_index, _id), _token.c_str());
    user_mgr::instance()->erase_uid(_thread_index,_id);
	return -1;
}

int tcp_netio::handle_run(time_t t)
{
	if ( t - _ctime > _service_timeout)
	{
        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: connection timeout", util::get_conn_id(_thread_index, _id), _token.c_str());
        tlogger::instance()->log("handler",fsk::level_t::debug_level(),_token,1,0);
		return -1;
	}
	//if ( _request.size() > 0)
	//{
	//	handle_recv();
	//}
    if ( _id < 0)
        return 0;

	get_send_msg(t);
    //string resp;
    //user_mgr::instance()->get_msgid(_thread_index,_id,t,resp);
    //proto_push::pack_v1_resp(resp,_resp);
    if ( _response.size() > 0)
    {
        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: run, unsend: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), _response.size());
        return handle_send();
    }


	return 0;
}

int tcp_netio::get_length()
{
    //header_struct_t *ph = (header_struct_t *)_request.data();
    //int length = ntohl(ph->_length);

    //return length;
    int length = ftsps::getlen((unsigned char*)_request.c_str());
    return length;
}

int tcp_netio::get_send_msg(time_t now)
{
	map<int,int> msglist;
	
	//int res = user_mgr::instance()->get_msgid(_thread_index,_id,now,pu_id,msgid);
	//get_msgid(int thread_index,int uid,time_t now,map<unsigned long long,int>& msg_list);
	user_mgr::instance()->get_msgid(_thread_index,_id,now,msglist);
    if ( msglist.size() > 0)
    {
        map<int,int>::iterator iter = msglist.begin();
        for ( ;iter!=msglist.end();iter++)
        {
            int msgid =iter->first;   
            if (true)
            {
                int appid;
                msg_struct* s_msg = NULL;
                int ret = msg_mgr::instance()->get_msg(msgid, &s_msg);
                if (ret != 0)
                {
                    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: fail to get msg or msg expired, msg_id: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), msgid);
                    tlogger::instance()->log("dpush",fsk::level_t::debug_level(),_token,msgid,0);
                    user_mgr::instance()->erase_msg(_thread_index,_id,msgid,appid);
                }
                else
                {
                    if (!util::is_sleepping_time()) {
                        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: get msg, msg_id: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), msgid);
                        string tresp;
                        proto_push::pack_push_v1(s_msg->_msg,tresp);
                        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: pack msg, msg_id: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), msgid);
                        // encrypt response
                        if ( ftsps::encrypt((unsigned char*)tresp.data(),tresp.length()) < 0)
                        {
                            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: fail to encrypt msg, msg_id: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), msgid);
                            tlogger::instance()->log("close",fsk::level_t::debug_level(),_token,101,0);
                            return -1;
                        }
                        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: encrypt msg, msg_id: %d", util::get_conn_id(_thread_index, _id), _token.c_str(), msgid);
                        _response.append(tresp);
                    }
                }
            }
        }
    }
        
        return 0;
    }
