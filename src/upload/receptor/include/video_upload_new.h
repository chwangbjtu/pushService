
#ifndef __VIDEO_UPLOAD_NEW__
#define __VIDEO_UPLOAD_NEW__

#include "file_info.h"
#include "i_accept_worker.h"

class video_upload_new:public i_accept_worker
{
	public:
		video_upload_new();
		video_upload_new(const video_upload_new& vu);
		virtual ~video_upload_new();
		virtual i_accept_worker* get_clone();

		virtual int process_header(request_t& http_req, char*& precv, long long& len, long long& data_len, string& resp); //, void*& pv);
		virtual int process_header(request_t& http_req, char*& precv, long long& len, long long& data_len,string& tid,string& resp) ;
		virtual int process_header(request_t& http_req, string& tid,string& resp);
		virtual int process_body(request_t& http_req, char* precv, long long len, string& _resp);
		virtual int process_body(char const * const precv,long long len,string &task_id, string& resp);

		virtual int process_disconnect(request_t& header, string& reason); //, void* pinfo);
		virtual int process_response(string& resp);

		virtual int get_part_resp(string& uhash,string& resp);
		
		int parse_param(request_t& http_req,meta_data& data,file_info*& fin,string& resp);

		enum
		{
			PROCESSING,
			HAS_RESPONSE,
			HAS_SENDED
		}_has_resp;

};

#endif
