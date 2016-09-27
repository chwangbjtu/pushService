
#ifndef __DATA_MANAGER_H
#define __DATA_MANAGER_H

#include<string>
#include<map>
#include<pthread.h>

#include "file_info.h"
#include "path_manager.h"

class data_manager
{
	public:
		data_manager();
		data_manager(int d);
		~data_manager();

		int init(string& res);
		int reload();
		int reload_single_file(string& fname);

		//get the instance of this class
	//	static data_manager* get_instance();

		/*query whether a file exists,the @info is the file info if the file exits
		*return:
		*	0：exist -1：not exits
		*/
		int query_info(string& file_id,file_info*& info);

		//add a file info of one new file,@info is the specific information.
		int dispatch_info(string& file_id,file_info* info);

		//update the file info of a exist file already.
		int update_info(string& file_id,file_info* info);

		//delete a file info,
		int delete_info(string& file_id, string& val);

		//delay aging ,if a file upload not finish for long time then delete it.
		int delay_aging(map<string,file_info*> &aging_info);

		//when sync finished, the follow treat.
		//int finish_sync(std::string& file_id, bool bl);

		int get_new_fileinfo(meta_data& md, file_info*& fin);
		
		int get_info_count();

		int query_stats(string& result);
		int query_stats(string& tid,string& result);

		int get_send_metas();

	public:
		bool upload_send_state(string& taskid,int state);
		int pack(const string type,meta_data& data,string& resp);

	private:
	//	static data_manager* _instance;

		pthread_mutex_t _mutex_loading;
		map<string,file_info*> _loading_info;
		//map<string,file_info*> finish_info;
		long _delay_time;

		path_manager* _pm;
};

#endif
