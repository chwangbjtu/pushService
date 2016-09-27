
#include <iostream>
#include <stdio.h>
#include <fcntl.h>
#include "meta_file.h"
#include "meta_data.h"
#include "tigress_logger.h"

meta_file::meta_file()
{
}

meta_file::~meta_file()
{
}

int meta_file::pack_meta_data(meta_data& dm, string& fname)
{
	_meta_name = fname;
	dm.pack(_st);
	return 0;
}

int meta_file::parse_meta_data(meta_data& dm, string& fname)
{
	int ret = -1;
	if (0 == open(fname.c_str()) && 0 == get_section("meta", _st))
	{
		ret = dm.parse(_st);
		_st.clear();
	}

	return ret;
}

int meta_file::flush_to_disk()
{
	//set_st("meta", section);
	return write_disk();
}

int meta_file::write_disk()
{
	//int fd = open(_meta_name.c_str(), O_RDWR|O_CREAT|O_SYNC, S_IWRITE|S_IREAD); //open conflict with the class configure
	//FILE* f = fdopen(fd, "w");

	FILE* f = fopen(_meta_name.c_str(),"w");
	if(f == NULL)
	{
		KERROR("the meta file %s can not open", _meta_name.c_str())
		return -1;
	}
	if (-1 == fcntl(fileno(f), F_SETFL, O_SYNC))
	{
		KERROR("the meta file %s can not set to sync", _meta_name.c_str())
		return -1;
	}
	setbuf(f, NULL);

	int ret = -1;
	ret = fprintf(f, "[%s]\n", "meta");
	if (ret < 0)
	{
		KERROR("the meta file %s write fail", _meta_name.c_str())
		return -1;
	}

	map<string, string>::iterator sib = _st.begin();
	for( ; sib != _st.end(); ++sib)
	{
		if ((ret = fprintf(f, "%s = %s\n", sib->first.c_str(), sib->second.c_str())) < 0)
		{
			KERROR("the meta file %s write fail", _meta_name.c_str())
			return -1;
		}
	}
	fprintf(f, "\n");

	fclose(f);

	return 0;
}
