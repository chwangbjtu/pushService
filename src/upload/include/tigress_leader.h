
#ifndef __TIGRESS_LEADER__
#define __TIGRESS_LEADER__

#include "info_leader.h"
#include "video_get_leader.h"
//#include "video_post_leader.h"
#include "file_info.h"
#include "sync_leader.h"
#include "meta_data.h"
#include "mgmt_leader.h"

class tigress_leader
{
	public:
		~tigress_leader();
		static tigress_leader* get_instance();

		int start(std::string& res);
		int query_info(std::string& fileid, file_info*& info);
		int get_new_fileinfo(meta_data& md, file_info*& fin);
		int flush_to_disk(void* arg, char* pstart, int len); 
		int flush_meta_to_disk(void* arg);
		int delete_info(std::string& fileid, std::string& val);

		int query_version(string& val);	
		int query_stats(string& taskid,string& result);
		int query_stats(string& result);
	public:
		bool upload_send_state(string& taskid,int state);
	private:
		//tigress_leader():_vgl(NULL), _inl(NULL), _vpl(NULL), _sl(NULL), _ml(NULL) {}
		tigress_leader():_vgl(NULL), _inl(NULL), _sl(NULL), _ml(NULL) {}
		static tigress_leader* _instance;

		video_get_leader* _vgl;
		info_leader* _inl;
		//video_post_leader* _vpl;
		sync_leader* _sl;
		mgmt_leader* _ml;
};

#endif
