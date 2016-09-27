#ifndef __VEIDEO_ACCEPT_HANDLER__
#define __VEIDEO_ACCEPT_HANDLER__

#include <string>
#include <time.h>
#include "tcp_service.h"
#include "http_request.h"
#include "i_accept_worker.h"

#ifdef __MOCK_CLASS__
#include <gmock/gmock.h>
#endif

#define MAX_HEADER_SIZE 8192 //8K max header size
#define TIME_OUT 6*60*60 //_service_timeout

using namespace std;

class video_accept_handler:public netsvc::epoll_handler
{
	public:
		video_accept_handler();
		//video_accept_handler(unsigned int time_out);
		virtual ~video_accept_handler();

		virtual int handle_open(void *arg);
		virtual int handle_send(void);
		virtual int handle_recv(void);
		virtual int handle_close(void);

		virtual int handle_run(time_t tm);

		int process_message();
		int parse_header(string::size_type position);
		int process_upload(unsigned char* pstart, unsigned int len);
		int reset();
		int process_header();
		bool recv_finish();
		void printt(const char *p);

		#ifdef __MOCK_CLASS__
		MOCK_METHOD3(send, ssize_t(const void*buffer, size_t length, int flags));
		MOCK_METHOD3(recv, ssize_t(char *buffer, int length, int flags));
		#endif
	private:
		time_t _start_time;
		int _service_timeout;
		string _disconn_reason;
		string _path;

		string _recv;//the received string
		string _resp;//the response string
		unsigned int _send_pos;//send position
		fs::request_t _http_req;// struct of request http_header

		//
		char* _precv;//开始接收地址
		//void* _pvoid;//传递的参数
		i_accept_worker* _pworker;


		//Parse http header
		enum 
		{
			NO_HEADER,
			FOUND_HEADER
		}_find_header;//HEADER_FOUND: has found the header, NO_HEADER: has not found header
		//int _find_header;

		long long _msg_length;//total length,gcd+header len
		long long _msg_length1;//
		long long  _header_length;
		long long _recv_length;
		long long _data_length;
		long long _table_header_length;//http header len + table header len
		long long _ttlen;
		bool _responsed;
		bool _found_error;
		bool _upload_statuts;
		string _method;
};

#endif
