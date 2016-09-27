
#include <sstream>
#include <unistd.h>
#include "tigress_logger.h"
#include "tigress_conf.h"
#include "file_info.h"
#include "tigress_leader.h"
#include "ret_code.h"
#include "json.h"
#include "k_str.h"

const int META_FILE_SIZE = 4096;
const long long SYNC_BLOCK_SIZE = 20*1024*1024;
//const int _block_size = 256*1024;

file_info::file_info():_mmp_start(NULL), _status(UPLOAD_STOP), _reffer_count(1), _block_size(0), _current_block(0), _current_len(0), _file_fd(0), _meta_fd(0), _sync_offset(0), _PAGE_SIZE(4096)
{
	_sha.Reset();
	_file_suffix = ".down";
	tigress_conf::get_instance()->get_string_value("info_manager", "file_suffix", _file_suffix);
	_PAGE_SIZE = getpagesize();
}

file_info::~file_info()
{
	if (_mmp_start != NULL)
	{
		munmap((void*)_mmp_start, _meta._length);
		close(_file_fd);
		remove(_file_name.c_str());
		_mmp_start = NULL;
	}
}

int file_info::file_init(string& path, meta_data& md)
{
	int ret = -1;
//	struct stat buf;
	
	_meta = md;
	//_file_name = path + md._task_id+ _file_suffix +".tmp";
	//_meta_name = path + md._task_id+ ".meta";
	_file_name = path + md._uhash + _file_suffix +".tmp";
	_meta_name = path + md._uhash + ".meta";
	_sync_offset = md._offset;

	if (path.empty() ||  md._length <= 0)
	{
		KERROR("incorrect file information");
		return -1;
	}
/*
	if ((ret = stat(path.c_str(), &buf)) == -1)
	{
		if (errno != ENOENT || mkdir(path.c_str(),S_IRWXU) != 0) //  ~(errno==2&&mkdir()==0)  ENOENT ==  No such file or directory
		{
			KERROR("can not create directory for file %s ", md._file_id.c_str());
			return -1;
		}
	}
*/
	if ((_file_fd = open(_file_name.c_str(), O_RDWR|O_CREAT, S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH)) == -1)
	{
		KERROR("can not open the new file %s ", md._file_id.c_str());
		return -1;
	}
	if ((ret = posix_fallocate(_file_fd, 0, md._length)) != 0) //Pre-allocate disk space 
	{
		KERROR("can not allocate disk space for the new file %s ", md._file_id.c_str());
		return -1;
	}

	if ((_meta_fd = open(_meta_name.c_str(), O_RDWR|O_CREAT, S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH)) == -1)
	{
		KERROR("can not open the new meta file for %s ", md._file_id.c_str());
		return -1;
	}
	if ((ret = posix_fallocate(_meta_fd, 0, META_FILE_SIZE)) != 0) //Pre-allocate disk space 
	{
		KERROR("can not allocate disk space for the new meta file for %s ", md._file_id.c_str());
		return -1;
	}

	_mmp_start = (char*)mmap64(NULL, md._length, PROT_READ|PROT_WRITE, MAP_SHARED, _file_fd, 0);
	if (_mmp_start == MAP_FAILED)
	{
		_mmp_start = NULL;
		KERROR("can not create memory file mapping for the new file %s ", md._task_id.c_str());
		return -1;
	}
	
	return 0;
}

int file_info::file_ready(string& res)
{
	int ret = -1;
	//如果status等于UPLOAD_STOP时，给_status赋值为UPLOAD_READY，并返回true
	//if (__sync_bool_compare_and_swap(&_status, UPLOAD_STOP, UPLOAD_READY))
	if ( _status != UPLOAD_FINISH)
	{
		ret = 0;
		_meta._last_time = time(NULL);
		KINFO("the file %s is ready to upload", _meta._task_id.c_str())
	}
	else
	{
		KERROR("the file %s duplicate to upload", _meta._task_id.c_str())
		switch(_status)
		{
			case UPLOAD_READY:
				res = "the file is been ready to upload";
				break;
			case UPLOAD_RECEIVING:
				res = "the file is uploading now";
				break;
			case UPLOAD_FINISH:
				res = "the file has uploaded finish";
				break;
			case UPLOAD_DELETE:
				res = "the file just been deleted";
				break;
			default:
				res = "unknown reason";
		}
	}

	return ret;
}

int file_info::file_ready_end(bool bl)
{
//	if (!bl)
//	{
	KINFO("the file %s upload from ready to stop", _meta._task_id.c_str())
	__sync_bool_compare_and_swap(&_status, UPLOAD_READY, UPLOAD_STOP);
//	}

	return 0;
}

int file_info::file_begin()
{
	int ret = -1;

	if (__sync_bool_compare_and_swap(&_status, UPLOAD_READY, UPLOAD_RECEIVING))
	{
		ret = 0;
		__sync_fetch_and_add(&_reffer_count, 1);
		_meta._last_time = time(NULL);
		KINFO("the file %s begin to upload", _meta._task_id.c_str())
	}
	else
		KINFO("the file %s begin to upload fail", _meta._task_id.c_str())

	return ret;
}

int file_info::file_update(char* pstart, long long len) //has a logger in the video_upload.cpp
{
	if (len <= 0)
	{
		return 0;
	}
	/*
	if (_status != UPLOAD_RECEIVING)
	{
		KERROR("the file %s is not in receiving",  _meta._task_id.c_str())
		return -1;
	}
	*/
	
	_meta._offset += len;
	_meta._last_time = time(NULL);
	_meta._sha_offset = _meta._offset;
	/*
	char* ps = pstart;
	if (_current_len + len >= _block_size)
	{
		while ((_meta._offset - _meta._sha_offset + _current_len) >= _block_size)
		{
			unsigned int plen = _block_size - _current_len;
			
			_sha.Update((unsigned char*)ps, plen);
			ps += plen;
			_sha.Final();
			_sha.GetBack(_meta._sha_middle);
			string dig;
			if ( !_vs.empty())
			{
				fs::byte2hexstr((const char*)_meta._sha_middle, 20, dig);
				if (dig != _vs[_current_block])
				{
					KERROR("the file %s check fail", _meta._file_id.c_str())
					return -1;
				}
			}

			++_current_block;
			_meta._sha_offset += _block_size; 
			_current_len = 0;//len - plen;

			_sha.Reset();
		}

		_current_len = _meta._offset - _meta._sha_offset;
		_sha.Update((unsigned char*)ps, _current_len);
		_sha.GetBack(_meta._sha_middle);
	}
	else
	{
		_current_len += len;
		_sha.Update((unsigned char*)ps, len);
	}
	*/

	if (_meta._offset == _meta._length)
	{
		/*
		_sha.Final();
		_sha.GetBack(_meta._sha_middle);
		string dig;
		if ( !_vs.empty())
		{
			fs::byte2hexstr((const char*)_meta._sha_middle, 20, dig);
			if (dig != _vs[_current_block])
			{
				KERROR("the file %s check fail", _meta._file_id.c_str())
				return -1;
			}
		}
		*/
		_meta._sha_offset = _meta._offset;
		//file_finish();
	}

	file_flush(pstart, len);
	return 0;
}

int file_info::file_finish()
{
	int ret = -1;
	int ct =  __sync_fetch_and_and(&_reffer_count, (~0x0));
	if (ct == 2) // no sync disk
	{
		ret = 0;
	}
	return ret;
}

bool file_info::send_not_over()
{
	bool ret = false;
	if (_meta._sha_offset == _meta._length && _meta._send_to_maze != send_over)
	{
		ret = true;
	}

	return ret;
}

bool file_info::file_recv_over()
{
	bool res = false;
	if ( _meta._sha_offset == _meta._length)
	{
		res = true;
	}

	return res;
}

int file_info::file_end()
{
	int ret = 0;
	if (_meta._sha_offset == _meta._length)
	{
		//__sync_bool_compare_and_swap(&_status, UPLOAD_RECEIVING, UPLOAD_FINISH);
		_status = UPLOAD_FINISH;
		//remove(_meta_name.c_str()); // modify 12.28
	}
	else
	{
		ret = -1;
		KINFO("the file %s upload stop unfinished,offset : %d,length %d", _meta._uhash.c_str(),_meta._offset,_meta._length)
		//__sync_bool_compare_and_swap(&_status, UPLOAD_RECEIVING, UPLOAD_STOP);
		_status = UPLOAD_STOP;
	}
	__sync_fetch_and_sub(&_reffer_count, 1);

	return ret;
}

int file_info::flush_meta()
{
	tigress_leader::get_instance()->flush_meta_to_disk(this);
	return 0;
}

int file_info::file_flush(char* pstart, int len) //called by file_update
{
	long long diff = _meta._sha_offset - _sync_offset;

//	KINFO("write to disk start %lld, len is %d", (long long)(pstart), len)
	if (_meta._sha_offset == _meta._length || diff >= SYNC_BLOCK_SIZE)
	{
		long long w_len = pstart - _mmp_start + len - _sync_offset;
		if (_meta._sha_offset != _meta._length)
			w_len = (w_len / _PAGE_SIZE) * _PAGE_SIZE;
		
		tigress_leader::get_instance()->flush_to_disk(this, (_mmp_start + _sync_offset), w_len);
		_sync_offset += w_len;
		__sync_fetch_and_add(&_reffer_count, 1); // _reffer_count++;
	}
	else
	{
		msync(pstart, len, MS_ASYNC);
	}

	return 0;
}

int file_info::file_flush_finish(char* pstart, int len)
{
	//_sync_finish_offset = pstart - _mmp_start + len;
	long long sync_len = pstart - _mmp_start + len;
	if (sync_len == _meta._length)
	{
		KINFO("the file %s upload finish", _meta._task_id.c_str())
		munmap((void*)_mmp_start, _meta._length);
		_mmp_start = NULL;
		close(_file_fd);
		string str = _file_name.substr(0, _file_name.rfind('.'));
		rename(_file_name.c_str(), str.c_str());
		_file_name = str;
		close(_meta_fd);
	}
	__sync_fetch_and_sub(&_reffer_count, 1); // _reffer_count--;
	return 0;
}

int file_info::file_delete()
{
	int ret = -1;
	//int ct = __sync_sub_and_fetch(&_reffer_count, 1);
	//__sync_lock_test_and_set(&_status, UPLOAD_DELETE);
	
	if(_meta._length == _meta._offset)
	{
		if (_mmp_start != NULL)
		{
			munmap((void*)_mmp_start, _meta._length);
			_mmp_start = NULL;
			close(_file_fd);
			close(_meta_fd);
			ret = 0;
		}
	}
	else
	{
		time_t now = time(NULL);
		if ( now - _meta._last_time > 3600) // 1 hour
		{
			if (_mmp_start != NULL)
			{
				munmap((void*)_mmp_start, _meta._length);
				_mmp_start = NULL;
				close(_file_fd);
				close(_meta_fd);
				ret = 0;
			}
		}
		else
		{
			ret = 1;
		}
	}

	return ret;
}

bool file_info::file_aging(int dtime)
{
	if ((time(NULL) - _meta._last_time) > dtime && _status != UPLOAD_DELETE && _reffer_count == 1 && _status != UPLOAD_FINISH)
		return true;

	return false;
}

int file_info::file_reload(meta_data& md, string& name)
{
	int ret = -1;

	do
	{
		_meta = md;
		_sha.Reset();
		_sync_offset = md._sha_offset;
		if (md._sha_offset == md._length)
		{
			_status = UPLOAD_FINISH;
			_meta_name = name;
			_file_name = name.substr(0, name.find(".meta")) + _file_suffix;
			if ((_file_fd = open(_file_name.c_str(), O_RDWR | O_EXCL)) == -1)
			{
				break;
			}
			close(_file_fd);
			ret = 0;
		}
		else if (md._sha_offset < md._length)
		{
			_status = UPLOAD_STOP;
			_meta_name = name;
			_file_name = name.substr(0, name.find(".meta" )) + _file_suffix + ".tmp";
			if ((_file_fd = open(_file_name.c_str(), O_RDWR, S_IWRITE|S_IREAD)) == -1)
			{
				break;
			}
			if ((_meta_fd = open(_meta_name.c_str(), O_RDWR, S_IWRITE|S_IREAD)) == -1)
			{
				close(_file_fd);
				break;
			}
			_mmp_start = (char*)mmap(NULL, md._length, PROT_READ|PROT_WRITE, MAP_SHARED, _file_fd, 0);
			if (_mmp_start == MAP_FAILED)
			{
				_mmp_start = NULL;
				close(_file_fd);
				close(_meta_fd);
				break;
			}
			ret = 0;
		}
		else
		{
			break;
		}
	}
	while(0);

	return ret;
}

int file_info::file_stat(string& result)
{
	stringstream sstr;
	result += _meta._file_id + "," + _meta._file_name + ",";
	switch (_status)
	{
		case UPLOAD_READY:
			result += "UPLOAD_READY,";
			break;
		case UPLOAD_RECEIVING:
			result += "UPLOAD_RECEIVING,";
			break;
		case UPLOAD_STOP:
			result += "UPLOAD_STOP,";
			break;
		case UPLOAD_FINISH:
			result += "UPLOAD_FINISH,";
			break;
		default:
			result += "unknown status,";
			break;
	}
	sstr<<_meta._length;
	sstr<<",";
	sstr<<_meta._sha_offset;
	result += sstr.str();

	return 0;
}

int file_info::file_stat_new(string& result)
{
	pandaria::json jn;
	jn.add("taskid",_meta._task_id);
	jn.add("fileid",_meta._file_id);
	jn.add("filename",_meta._file_name);
	jn.add("filelength",_meta._length);
	jn.add("offset",_meta._offset);
	jn.add("createtime",(int)_meta._create_time);
	jn.add("lasttime",(int)_meta._last_time);
	jn.add("sendtomaze",_meta._send_to_maze);
	jn.add("ret","0");

	result = jn.to_formated_str();
	return 0;
}



