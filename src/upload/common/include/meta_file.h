
#ifndef __META_FILE__
#define __META_FILE__

#include "k_configure.h"
#include "file_info.h"

class meta_file:public fs::k_configure
{
public:
	meta_file();
	~meta_file();
	int pack_meta_data(meta_data& dm, string& fname);
	int parse_meta_data(meta_data& dm, string& fname);

	int flush_to_disk();
	int write_disk();
public:
	map<string, string> _st;
	string _meta_name;
};

#endif
