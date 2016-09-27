#include <sys/time.h>
#include <sstream>
#include "k_str.h"
#include "http_netio.h"
#include "dbg.h"
#include "http_dispatcher.h"
//#include "http_response.h"
#include "configure.h"
#include "util.h"
//#include "tlogger.h"

using namespace std;

http_netio::http_netio():
	_snd_len(0),
	_ctime(time(NULL)),
	_proto_len(0),
	_content_length(-1),
	_header_length(0)
{
	_timeout = configure::instance()->get_http_timeout();
}

http_netio::~http_netio()
{
}
int http_netio::handle_recv()
{
	const int BUF_LEN = 2048;
	char buf[BUF_LEN] = {0};
	ssize_t recv_len = 0;
	while((recv_len = ::recv(sock(), buf, BUF_LEN, 0)) > 0) 
	{
		_request.append(buf, recv_len);
	}
	if(recv_len < 0 && (errno != EAGAIN && errno != EWOULDBLOCK)) 
	{
		return -1;
	} 
	else if(recv_len == 0 && _request.empty()) 
	{
		return -1;
	}

    _ctime = time(NULL);

	if ( recv_finished())
	{
		if(http_dispatcher::instance()->process(_request, peer_ip(),_response) < 0) 
		{
            _response = util::instance()->get_http_400_resp();
            return handle_send();
			//return -1;//close socket
		} 
		else
		{
			return handle_send();
		}
	} 
	else
	{
		return 0;//continue to receive
	}
	return -1;
}

int http_netio::handle_open(void *arg)
{
	return 0;
}

int http_netio::handle_send()
{
	if(_response.length() == 0) 
	{
		return 0;
	}
	size_t resp_len = _response.length();
	while (_snd_len < resp_len) 
	{
		ssize_t n = ::send(sock(), _response.data()+_snd_len,resp_len-_snd_len, 0);
		if(n > 0)
		{
			_snd_len += (size_t)n;
		}
		else if(n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK ))
		{
			/* action blocked */
			return 0;
		}
		else 
		{
			break;
		}
	}
	//send all response
	_response.clear();
	return -1;
}
int http_netio::handle_close()
{
	return -1;
}

int http_netio::handle_run(time_t t)
{
	if((t - _ctime) > _timeout) 
	{
        //_data = util::instance()->get_error_resp();
		//return -1;
		_response = util::instance()->get_http_408_resp();
        return handle_send();
	}

	return 0;
}

bool http_netio::recv_finished()
{
	if ( _request.compare(0, 4, "GET ", 4) == 0)
	{
		return get_finished();
	} 
	else if (_request.compare(0, 5, "POST ", 5) == 0) 
	{
		return post_finished();
	} 
	else
	{
		return false;
	}
}

int http_netio::extract_between(const std::string& data, std::string& result, const std::string& separator1, const std::string& separator2)
{
	std::string::size_type start, limit;

	start = data.find(separator1, 0);

	if ( std::string::npos != start)
	{
		start += separator1.length();
		limit = data.find(separator2, start);
		if ( std::string::npos != limit)
		{
			result = data.substr(start, limit - start);
			return 0;
		} 

	}
	return -1;
}

bool http_netio::post_finished()
{
	if ( _content_length <0)
	{
		std::string::size_type pos; 
		pos = _request.find("\r\n\r\n",0);
		if (string::npos == pos )
		{
			return false;
		}
		_header_length = pos +4;
		std::string content_len_str; 
		int ret = 0;
        /*
		string content_lenth = "Content-Length: ";
		ret = extract_between(_request, content_len_str, content_lenth);//in this service http-post-header must have Content-Length:
		if ( ret < 0 )
		{
            return false;
  		} 
        */
        ///
        string content_lenth = "Content-Length: ";
        string content_lenth1 = "Content-length: ";
        ret = extract_between(_request, content_len_str, content_lenth1);
        if (ret < 0)
        {
           ret = extract_between(_request, content_len_str, content_lenth); 
        }
        if (ret < 0)
        {
            return false;
        }
        ///
		if (is_digit(content_len_str) <0) 
		{
			return false;
		}
		_content_length = atoi(content_len_str.c_str());
         }
	if ( (_content_length + _header_length ) > _request.length())
	{
		return false;
	} 
	return true;
}

bool http_netio::get_finished()
{
	std::string::size_type pos; 
	pos = _request.rfind("\r\n\r\n");
	if (string::npos == pos ) 
	{
		return false;
	} 
	else 
	{
		return true;
	}
}

int http_netio::is_digit(const string & str)
{
	int size = str.length();
	if ( size == 0)
	{
		return -1;
	}
	
	const char DIGIT_MAX = '9';
	const char DIGIT_MIN = '0';
	int i = 0;
	int ret = 0;
	
	while ( i < size )
	{
		if ( str[i] <= DIGIT_MAX && str[i] >= DIGIT_MIN )
		{
			i++;
			continue;
		}
		else 
		{
			ret = -1;
			break;
		}
	}

	return ret;
}




