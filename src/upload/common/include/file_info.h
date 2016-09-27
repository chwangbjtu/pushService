
#ifndef __FILE_INFO
#define __FILE_INFO

#include <vector>
#include<string>
#include<time.h>
#include<fcntl.h>
#include<sys/stat.h>
#include<sys/mman.h>
#include<errno.h>
#include "sha_1.h"
#include "meta_data.h"

using namespace std;
/*
#define FILEID_PRE_LENGTH  40
#define FILENAME_PRE_LENGTH  32
#define FILEPATH_PRE_LENGTH  32
*/

class file_info
{
	public:
		file_info();
		~file_info();//有关资源的释放都在这里做
		int file_init(string& path, meta_data& md);
		int file_reload(meta_data& md, string& name);

		int file_ready(string& res);
		int file_ready_end(bool bl);
		int file_begin();
		int file_update(char* pstart, long long len);
		int file_finish();
		int file_end();

		int file_flush(char* pstart, int len);
		int file_flush_finish(char* pstart, int len);
		int flush_meta();

		int file_delete(); // return 1 need to wait, 0 delete success -1 deleted but error occur
		bool file_aging(int dtime);

		int file_stat(string& result);
		
		int file_stat_new(string& result);

		bool send_not_over();

		bool file_recv_over();

	public:
		meta_data _meta;
		SHA_1 _sha;

		char* _mmp_start; //start address of the mmap
		
		//bool _uploading; //whether the file is uploading
		volatile enum
		{
			UPLOAD_READY = 0,
			UPLOAD_RECEIVING,
			UPLOAD_STOP,
			UPLOAD_FINISH,
			UPLOAD_DELETE
		}_status; //file status
		int _reffer_count;
		
		vector<string> _vs;
		long long _block_size;
		int _current_block;
		int _current_len;
	public:
		string _meta_name; //meta file name
		string _file_name; //full name
		string _file_suffix;
		int _file_fd;
		int _meta_fd;
		long long _sync_offset; //the offset of sync that to do
		//long long _sync_finish_offset; //the offset of sync taht has finished
		int _PAGE_SIZE;
};

#endif
