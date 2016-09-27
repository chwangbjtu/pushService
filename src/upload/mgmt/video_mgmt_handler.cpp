
#include "tigress_logger.h"
#include "video_mgmt_handler.h"
#include "mgmt_worker_manager.h"

video_mgmt_handler::video_mgmt_handler(): _send_pos(0)
{

}

video_mgmt_handler::~video_mgmt_handler()
{

}

int video_mgmt_handler::handle_open(void* arg)
{
	return 0;
}

int video_mgmt_handler::handle_send(void)
{
	ssize_t ret =0;
	const char* pstart = _resp.c_str();
	unsigned int length  = _resp.size();

	if (_resp.empty())
	{
		return 0;
	}
	while ((ret = send(pstart + _send_pos, length - _send_pos, 0) ) > 0)
	{
		_send_pos += ret;
	}
	if ((ret < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || ret == 0)
	{
		return -1;
	}
	if (_send_pos == length)
	{
		return -1;
	}

	return 0;
}

int video_mgmt_handler::handle_recv(void)
{
	ssize_t recv_len = 0;
	char buf[1024] = {0};

	while ((recv_len = recv(buf, 1024, 0)) > 0)
	{
		_recv.append(buf, recv_len);
	}
	if ((recv_len < 0 && errno != EWOULDBLOCK && errno != EAGAIN) || recv_len == 0)
	{
		return -1;
	}

	if (_recv.find("\r\n\r\n") != _recv.npos)
	{
		int ret = ( static_cast<mgmt_worker_manager*>(userarg()) )->get_response(_recv, _resp);
		if (ret != 0)
		{
			return -1;
		}
	}
	else
	{
		if (_recv.size() > MAX_MGMT_HEADER_SIZE)
		{
			char s[40] = {0};
			in_addr addr;
			addr.s_addr = peer_ip();
			char* s1 = inet_ntoa(addr);
			strcpy(s, (const char*)s1);
			KERROR("an illegal mgmt http packets from %s", s)
			return -1;
		}
	}

	return 0;
}

int video_mgmt_handler::handle_close(void)
{
	return 0;
}

int video_mgmt_handler::handle_run(time_t tm)
{
	return 0;
}
