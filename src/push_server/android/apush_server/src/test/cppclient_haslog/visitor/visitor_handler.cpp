#include <sstream>
#include"dbg.h"
#include "soc_mgr.h"
#include "en_interface.h"
#include "proto_process.h"
#include "proto_struct.h"
#include "proto_constant.h"
#include "proto_dispatcher.h"
#include "visitor_handler.h"

//using fs::http_req;

visitor_handler::visitor_handler()
{
    int fd1 = soc_mgr::instance()->get_id1();
    //DBG_INFO("fd1:%d",fd1);
    
	_ctime = time(NULL);
    _ret = -1;
    _send_pos = 0;
    _htbt_interval = soc_mgr::instance()->get_htbt_interval();
}

visitor_handler::~visitor_handler()
{
    
}

int visitor_handler::handle_open(void *arg)
{
    _fd = soc_mgr::instance()->get_id();
    string msg = soc_mgr::instance()->get_msg(_fd);
    _req = msg;
    unsigned int* pi = (unsigned int*)_req.data();
    pi ++;
    DBG_INFO("len:%x,%d",*pi,*pi);
    stringstream ss;
    ss<<msg;
    string tt;
    tt = ss.str();
    //
    DBG_INFO("login size:%d",tt.length());
    ftsps::encrypt((unsigned char*)tt.data(),tt.length());
    _req = tt;
    DBG_INFO("%d",_fd);
    return 0;
}

int visitor_handler::handle_send(void) // whether to return -1
{
    ///*
    ssize_t ret=0;

    if (_req.size() == 0)
    {
        return 0;
    }

    while ((ret = send(_req.c_str() + _send_pos, _req.size() - _send_pos, 0) ) > 0)
    {
		if ( ret > 0)
		{
        	_send_pos += ret;
		}
		else if(ret < 0 && (errno == EAGAIN || errno == EWOULDBLOCK ))
		{
			return 0;
		}
		else
		{
			break;
		}
    }

    if ( _send_pos >= _req.size())
    {
    	_req.clear();
        _send_pos = 0;
    }


    //*/

    return 0;
}

int visitor_handler::handle_recv(void)
{
    ///*
    char buf[1024] = {0};
    ssize_t recv_len = 0;
    string::size_type position;

    while ((recv_len = recv(buf,1024,0)) > 0)
    {
        _recv.append(buf,recv_len);
    }
    if ((recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || recv_len == 0)
    {
        DBG_ERROR("%d,%d",recv_len,errno);
        return -1;
    }

     int length = 0;
    if ( _recv.size() >= proto_header_len)
    {
        DBG_INFO("--------------%d",length);
        length = get_length();
        DBG_INFO("--------------%d",length);
    }

    if (length < 0 || length > 4096)
    {
        DBG_INFO("%d",length);
        return -1;
    }

    int res = 0;
    //while (_recv.size() > 0 && _recv.size() >= length + sizeof(header_struct_t) && res == 0 && length <= 4096)
    while (_recv.size() >= length && res == 0 && length != 0)
    {
        DBG_INFO("");
        string tresp;
        //if ( _req.size() == 0)
        {
            DBG_INFO("");
            int t = 0;
            if ( _recv.size() >= 16)
            {
                ftsps::decrypt((unsigned char*)_recv.data(),_recv.length());
            }
            string tt;
            tt = _recv.substr(16,_recv.size());
            //DBG_INFO("%s",tt.data());
            DBG_INFO("");
            res = proto_dispatcher::instance()->process(_recv, 0,0,_fd,tresp);
            DBG_INFO("%d,%d",res,tresp.size());
            if ( res == 0 && tresp.size() > 0)
            {
                ftsps::encrypt((unsigned char*)tresp.data(),tresp.length());
                _req.append(tresp);
            }
            else
            {
            }
            DBG_INFO("");
        }
        //else
        {
            /*
            DBG_INFO("");
            int t = 0;
            string tresp;
            res = proto_dispatcher::instance()->process(_recv, 0,0,_fd,tresp);
            if ( _recv.size() >= 16)
            {
                ftsps::encrypt((unsigned char*)_recv.data(),_recv.length());
            }
            if( _recv.size() > 16)
            {
                string str = _recv.substr(16,length);
                cout<<str<<endl;
            }
            if ( res == 0)
            {
                _req.append(tresp);
            }
            */
            
        }
        length = 0;
        if ( _recv.size() >= proto_header_len)
        {
            length = get_length();
            if ( length > 4096)
            {
                DBG_INFO("");
                return -1;
            }
        }

        if ( res != 0)
        {
            DBG_INFO("");
            return -1;
        }
    }
    

    _recv.clear();
    //*/
    
    return 0;
}

int visitor_handler::handle_close(void)
{
    DBG_ERROR("close %d",_fd);
    return -1;
}

int visitor_handler::handle_run(time_t tm)
{
    ///*
    //if ( tm - _ctime >= 10)
    //string msg = soc_mgr::instance()->get_msg(_fd);
    string msg = soc_mgr::instance()->get_push_msg(_fd);
    if ( tm - _ctime >= _htbt_interval || msg.size() > 0)
    {
        if ( msg.size() == 0)
            msg = soc_mgr::instance()->get_msg(_fd);
        ///*
        if ( _req.size() == 0)
        {
            _req = msg;
            DBG_INFO("");
            ftsps::encrypt((unsigned char*)_req.data(),_req.length());
        }
        else
        {
            ftsps::encrypt((unsigned char*)msg.data(),msg.length());
            _req.append(msg);
        }
        _ctime = tm;
        handle_send();
        //*/
    }
    
    //*/
    //
    //if ( _req.size() > 0)
    //    handle_send();

    return 0;
}

int visitor_handler::get_length()
{
    //header_struct_t *ph = (header_struct_t *)_recv.data();
    //int length = ntohl(ph->_length);
    int length =  ftsps::getlen((unsigned char*)_recv.c_str());

    return length;
}



