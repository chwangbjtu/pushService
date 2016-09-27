
#ifndef __VIDEO_PROG_NEW__
#define __VIDEO_PROG_NEW__

#include "i_accept_worker.h"
#include "file_info.h"

#define MESSAGE_BUFFER_SIZE 1   //800K

class video_prog_new:public i_accept_worker
{
	public:
		video_prog_new();
		virtual ~video_prog_new();
		video_prog_new(const video_prog_new& vp);
		virtual i_accept_worker* get_clone();

		virtual int process_body(char const * const precv,long long len,string &task_id, string& resp);
		virtual int process_header(request_t& http_req, string& tid,string& resp);
		int parse_message(string& s_body, string& resp, meta_data& data, file_info*& f_info,string& callback);

		int ppack(int ret,meta_data& data,string callback,file_info*& f_info,string& resp);
		int check_uhash( meta_data& md, file_info*& f_info);

		//bool _has_resp;
	private:
		enum
		{
			PROCESSING,
			HAS_RESPONSE,
			HAS_SENDED
		}_has_resp;
};

#endif
