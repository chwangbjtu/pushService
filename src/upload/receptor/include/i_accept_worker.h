
#ifndef __I_ACCEPT_WORKER__
#define __I_ACCEPT_WORKER__

#include "http_def.h"
#include "meta_data.h"
//#include "http_response.h"

//#define MESSAGE_BUFFER_SIZE 1536   //1.5k

using namespace fs;

class i_accept_worker
{
	public:
		i_accept_worker() {} //:_body_len(0),_recv_len(0) {}
		virtual ~i_accept_worker() {}
		i_accept_worker(const i_accept_worker& aw)
		{
			//this->_body_len = aw._body_len;
			//this->_recv_len = aw._recv_len;
		}
		virtual i_accept_worker* get_clone(){return NULL;}

		virtual int process_header(request_t& http_req, char*& precv, long long& len, string& resp){return -1;}
		virtual int process_header(request_t& http_req, char*& precv, long long& len,string& resp,string tid) {return -1;}

		virtual int process_header(request_t& http_req, char*& precv, long long& len, long long& data_len, string& resp){return -1;}
		virtual int process_header(request_t& http_req, char*& precv, long long& len, long long& data_len,string& resp,string tid) {return -1;}

		virtual int process_header(request_t& http_req, string& tid,string& resp){return -1;}
		
		virtual int process_body(request_t& http_req, char* precv, long long len, string& resp){return -1;}

		virtual int process(string& body,string& resp){return -1;}
		virtual int process_body(char const * const precv,long long len,string &task_id, string& resp){return -1;}
		virtual int process_disconnect(request_t& header, string& reason){return -1;}
		virtual int process_response(string& resp) {return -1;}
		virtual int get_part_resp(string& uhash,string& resp){return -1;}
		virtual int pack(const int status,meta_data& data,const string protocal,string callback,string& resp);
		int pack(const string type,meta_data& data,string status,string& resp);
		//virtual bool has_response();

	public:
		//unsigned long _body_len;
		//unsigned long _recv_len;
};

#endif
