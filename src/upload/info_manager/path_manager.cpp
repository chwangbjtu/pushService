
#include <sys/statvfs.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include "path_manager.h"
#include "tigress_conf.h"
#include "tigress_logger.h"

path_manager::path_manager():_unuse_rate(0.01) 
{

}

path_manager::~path_manager()
{

}

int path_manager::init(string& res)
{
	string paths ="" ;
	string pth;
	size_t begin = 0;
	size_t end = string::npos;

	int ret = 0; // must be 0
	ret |= tigress_conf::get_instance()->get_string_value("info_manager", "file_paths", paths);
	ret |= tigress_conf::get_instance()->get_float_value("info_manager", "disk_unuse_rate", _unuse_rate);
	if (0 != ret)
	{
		res = "path_manager read configure file fail";
		return -1;
	}

	while ((end = paths.find(" ", begin)) != string::npos)
	{
		pth.assign(paths, begin, end - begin);
		begin = end + 1;
		if (pth.size() > 0)
		{
			_vpath.push_back(pth);
		}
		pth.clear();
	}
	if (begin < end)
	{
		pth.assign(paths, begin, end - begin);
		_vpath.push_back(pth);
	}

	if (_vpath.empty())
	{
		res = "the file_paths in configure file is empty";
		return -1;
	}

	ret = 0;
	DIR* d = NULL;
	struct stat buf;
	vector<string>::iterator iter;

	for (iter = _vpath.begin();iter != _vpath.end();++iter)
	{
		if ((*iter)[(*iter).size()-1] != '/')
		{
			(*iter).append("/");
		}

		if (-1 == stat((*iter).c_str(), &buf))
		{
			if (errno != ENOENT || mkdir((*iter).c_str(),S_IRWXU | S_IRWXG | S_IROTH) != 0) //  ~(errno==2&&mkdir()==0)  ENOENT ==  No such file or directory
			{
				res = "no such  directory ";
				res += (*iter).c_str();
				res += " and can not create it";
				ret = -1;
				break;
			}
		}

		d = opendir((*iter).c_str());
		if (NULL == d)
		{
			res = "can not open the path ";
			res += (*iter).c_str();
			res += " errno is ";
			res += strerror(errno);
			ret = -1;
			break;
		}
		else
		{
			closedir(d);
		}
	}

	return ret;
}

int path_manager::get_file_path(long long len, std::string& path)
{
	int ret = -1;
	struct statvfs buf;
	long long totaldisk = 0;
	long long availdisk = 0;

	if (0 == statvfs(_vpath[0].c_str(), &buf))
	{
		totaldisk = (buf.f_bsize >> 10) * buf.f_blocks;
		availdisk = ((buf.f_bsize >> 10) * buf.f_bavail) - (len >> 10);
	}
	else
	{
		KERROR("statfs error with errno %s", strerror(errno));
	}

	if (availdisk > (totaldisk * _unuse_rate))
	{
		ret = 0;
	}

	//path = "./"; //////?????

	path = _vpath[0];
	return ret;

}
