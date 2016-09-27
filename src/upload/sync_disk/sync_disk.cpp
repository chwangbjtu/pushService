
#include <errno.h>
#include "sync_disk.h"
#include "file_info.h"
#include "tigress_logger.h"

sync_disk::sync_disk():_fin(NULL), _pstart(NULL), _len(0)
{

}
sync_disk::~sync_disk()
{

}

int sync_disk::init(void* pf, char* pstart, int len)
{
	_fin = pf;
	_pstart = pstart;
	_len = len;

	_mfile.pack_meta_data((static_cast<file_info*>(pf))->_meta, (static_cast<file_info*>(pf))->_meta_name);
	return 0;
}

int sync_disk::flush_meta_to_disk()
{
	if (0 != _mfile.flush_to_disk())
	{
		KERROR("the meta file %s sync fail with errno %s ", (static_cast<file_info*>(_fin))->_meta._file_id.c_str(), strerror(errno))
	}
	
	return 0;
}

//try catch can not catch the system error, they were by signal

int sync_disk::flush_to_disk()
{
//	KINFO("the video file %s sync  with  start is %lld len is %d ", (static_cast<file_info*>(_fin))->_meta._file_id.c_str(),  (long long)_pstart, (int)_len)
	void* vd = (void*)_pstart;
	if (0 != msync(vd, _len, MS_SYNC))
	{
		KERROR("the video file %s sync fail with errno %d  %s start is %lld len is %d ", (static_cast<file_info*>(_fin))->_meta._file_id.c_str(), errno, strerror(errno), (long long)_pstart, (int)_len)
	}
	
	if (0 != _mfile.flush_to_disk())
	{
		KERROR("the meta file %s sync fail with errno %s ", (static_cast<file_info*>(_fin))->_meta._file_id.c_str(), strerror(errno))
	}
	(static_cast<file_info*>(_fin))->file_flush_finish(_pstart, _len);
	/*
	try
	{
		_mfile.flush_to_disk();
		msync(_pstart, _len, MS_SYNC);
		((file_info*)_fin)->file_flush_finish(_pstart, _len);
	}
	catch(...)
	{
		//KERROR("when file %s flush to disk error occur!", ((file_info*)_fin)->_meta_name)
	}
	*/
	return 0;
}
