
#ifndef __VIDEO_UPLOAD_XML__
#define __VIDEO_UPLOAD_XML__

#include "i_accept_worker.h"

class video_upload_xml:public i_accept_worker
{
	public:
		video_upload_xml();
		video_upload_xml(const video_upload_xml& vu);
		virtual ~video_upload_xml();
		virtual i_accept_worker* get_clone();

		virtual int process_header(request_t& http_req, char*& precv, long long& len, string& resp); //, void*& pv);
		virtual int process_header(request_t& http_req, string& tid,string& resp);
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
