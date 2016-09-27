
#ifndef __VIDEO_UPLOAD_OPTIONS__
#define __VIDEO_UPLOAD_OPTIONS__

#include "i_accept_worker.h"

class video_upload_options:public i_accept_worker
{
	public:
		video_upload_options();
		video_upload_options(const video_upload_options& vu);
		virtual ~video_upload_options();
		virtual i_accept_worker* get_clone();

		virtual int process_header(request_t& http_req, char*& precv, long long& len, string& resp); //, void*& pv);
		virtual int process_body(request_t& http_req, char* precv, long long len, string& _resp);
		virtual int process_body(char const * const precv,long long len,string &task_id, string& resp);
		virtual int process_disconnect(request_t& header, string& reason); //, void* pinfo);
		virtual int process_response(string& resp);

	public:
		long long _body_len;
		long long _recv_len;
		void* _pv;

		enum
		{
			PROCESSING,
			HAS_RESPONSE,
			HAS_SENDED
		}_has_resp;

};

#endif
