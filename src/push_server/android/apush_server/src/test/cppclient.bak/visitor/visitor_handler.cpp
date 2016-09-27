#include"dbg.h"
#include "soc_mgr.h"
#include "visitor_handler.h"

//using fs::http_response;

visitor_handler::visitor_handler()
{
	_ctime = time(NULL);
    _ret = -1;
    _send_pos = 0;
}

visitor_handler::~visitor_handler()
{
}

int visitor_handler::handle_open(void *arg)
{
    _fd = soc_mgr::instance()->get_id();
    DBG_INFO("%d",_fd);
    return 0;
}

int visitor_handler::handle_send(void) // whether to return -1
{
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

	_req.clear();

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
    if ((recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || recv_len == 0)
    {
        DBG_ERROR("recv:%d",recv_len);
        return -1;
    }

    
    return 0;
}

int visitor_handler::handle_close(void)
{
    DBG_ERROR("close %d",_fd);
    return -1;
}

int visitor_handler::handle_run(time_t tm)
{
    string msg = soc_mgr::instance()->get_msg(_fd);
    if ( _req.size() == 0)
        _req = msg;
    else
        _req.append(msg);

    return 0;
}




