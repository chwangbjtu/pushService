#ifndef __META_DATA__
#define __META_DATA__

#include <map>
#include <string>

using namespace std;

class meta_data
{
public:
	//meta_data(int count);
	meta_data();
	~meta_data();
	meta_data& operator = (const meta_data& md);
	int pack(map<string, string>& mp);
	int parse(map<string, string>& mp);
public:
	string _file_id;
	string _file_name;
	string _hash_id;//客户端上传hashid
	string _uid;
	string _uhash;//userid + hashid
	string _task_id;//tigress生成taskid回应给客户端
	string _key;
	//string _file_hash; //_file_id may be not the info_hash, if they are same use _file_id 

	long long _offset;
	long long _length;
	long long _sha_offset;
	time_t _create_time;
	time_t _last_time;
	int _send_to_maze;

	//int _bitcount;
	//int* _bitmap;
	unsigned char _sha_middle[40];
	unsigned char _check[20];

};

#endif
