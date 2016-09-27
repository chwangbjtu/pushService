#ifndef __TCP_NETIO_H
#define __TCP_NETIO_H
#include <string>
#include "tcp_service.h"
using namespace std;

const unsigned int max_recv_packet = 512;

class tcp_netio :public netsvc::epoll_handler
{
public:
	tcp_netio();
	virtual ~tcp_netio(void);
	virtual int handle_open(void *arg);
	virtual int handle_send();
	virtual int handle_recv();
	virtual int handle_close();

	virtual int handle_run(time_t tm);
protected:
    int get_length();
	int get_send_msg(time_t now);
private:
    int     _id;//user index,arr index;
    int     _send_len;
    string _request;
    string _response;
    string _token;
    time_t  _ctime;
	int _service_timeout;
};

#endif //__TCP_NETIO_H

