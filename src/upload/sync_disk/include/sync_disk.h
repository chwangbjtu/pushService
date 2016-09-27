
#ifndef __SYNC_DISK__
#define __SYNC_DISK__

#include "meta_file.h"

class sync_disk
{
public:
	sync_disk();
	~sync_disk();

	int init(void* pf, char* pstart, int len);
	int flush_to_disk();
	int flush_meta_to_disk();
public:
	meta_file _mfile;
	void* _fin;
	char* _pstart;
	int _len;
};

#endif
