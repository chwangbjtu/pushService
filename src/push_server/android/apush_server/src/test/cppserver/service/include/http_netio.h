#ifndef __HTTP_NETIO_H
#define __HTTP_NETIO_H
#include <string>
#include "tcp_service.h"
using namespace std;

class http_netio :public netsvc::epoll_handler
{
public:
	http_netio();
	virtual ~http_netio(void);
	virtual int handle_open(void *arg);
	virtual int handle_send();
	virtual int handle_recv();
	virtual int handle_close();

	virtual int handle_run(time_t tm);
private:
	bool recv_finished();

	int extract_between(const std::string& data, std::string& result, const std::string& separator1, const std::string& separator2= "\r\n");

	bool post_finished();

	bool get_finished();

	int is_digit(const string & str);

private:
	string		_request;
	string		_response;
    string      _task_id;
    string      _oid;
    string      _data;
    string      _content_type;
    
	size_t		_snd_len;
	//time_t		_ctime;
    unsigned int _tid;
    unsigned long long   _ctime;
	size_t		_proto_len;
	int 			_timeout;
	int 			_content_length;
	int			_header_length;
    int     _width;
    int     _height;
};

#endif //__HTTP_NETIO_H

