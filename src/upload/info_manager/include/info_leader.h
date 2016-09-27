
#ifndef __INFO_LEADER__
#define __INFO_LEADER__

#include "data_manager.h"
#include "aging_treat.h"
#include "meta_data.h"

class info_leader
{
	public:
		info_leader();
		~info_leader();
		int start(string& res);//, void*& dm);

		int query_info(string& fileid, file_info*& info);
		int delete_info(string& fileid, string& val);
		int get_new_fileinfo(meta_data& md, file_info*& fin);
		int query_stats(string& taskid,string& result);
		int query_stats(string& result);
	public:
		bool upload_send_state(string& taskid,int state);
	private:
		data_manager* _dm;
		aging_treat* _aging;
		fsk::ktimer<fsk::ktimer_list> _timer;
};

#endif
