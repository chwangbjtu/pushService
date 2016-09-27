#include <iostream>
#include <sstream>
#include "meta_data.h"
#include "tigress_logger.h"
#include "k_str.h"
#include "sha_1.h"

using namespace std;

meta_data::meta_data():_file_id(""), _file_name(""), _offset(0), _length(0), _sha_offset(0), _last_time(0),_send_to_maze(0)//, _bitcount(0), _bitmap(NULL)
{
	_create_time = time(NULL);
	memset(_sha_middle, 0, 40);
	memset(_check, 0, 20);
}

meta_data::~meta_data()
{

}

meta_data& meta_data::operator = (const meta_data& md)
{
	this->_file_id = md._file_id;
	this->_task_id = md._task_id;
	this->_uid = md._uid;
	this->_hash_id = md._hash_id;
	this->_uhash = md._uhash;
	this->_file_name = md._file_name;
	this->_key = md._key;
	//this->_file_hash = md._file_hash;

	this->_offset = md._offset;
	this->_length = md._length;
	this->_sha_offset = md._sha_offset;
	this->_create_time = md._create_time;
	this->_last_time = md._last_time;
	this->_send_to_maze = md._send_to_maze;

	memmove(this->_sha_middle, md._sha_middle, 40);
	memmove(this->_check, md._check, 20);

	return *this;
}
/*
int meta_data::set_bitmap(int num)
{
	if (num <= _bitcount)
	{
		_bitmap[num >> 5] |= (1 << (num & 0x1f));
	}
	return 0;
}

int meta_data::get_bitmap(int& num)
{
	int i = 0, j = 0;
	bool bf = false;
	for (i;i < _bitcount;i++)
	{
		if (_bitmap[i] != 0xffffffff)
		{
			for (j = 0;j < 32;j++)
			{
				if (test_bitmap[(i << 32) + j] == 0)
				{
					break;
				}
			}
			if (j != 32)
			{
				bf = true;
				num = (i << 32) + j;
				break;
			}
		}
	}

	if(bf)
		return 0;
	else
		return -1;
}


int meta_data::clear_bitmap(int num)
{
}
*/

int meta_data::pack(map<string, string>& mp)
{
	stringstream st;
	string tmp;

	SHA_1 sha;
	sha.Reset();
	sha.Update((unsigned char*)_file_id.c_str(), _file_id.size());
	sha.Update((unsigned char*)_file_name.c_str(), _file_name.size());
	//sha.Update(&_offset, 8);
	sha.Update((unsigned char*)&_length, 8);
	sha.Update((unsigned char*)&_sha_offset, 8);
	sha.Update((unsigned char*)&_last_time, 8);
	sha.Final();
	sha.GetHash(_check);
	mp.insert(pair<string, string>("file_id", _file_id));
	mp.insert(pair<string, string>("taskid",_task_id));
	mp.insert(pair<string, string>("file_name", _file_name));
	mp.insert(pair<string, string>("key",_key));
	mp.insert(pair<string,string>("uid",_uid));
	mp.insert(pair<string,string>("hashid",_hash_id));
	mp.insert(pair<string,string>("uhash",_uhash));
	//mp.insert(makepair<string, string>("file_hash", _file_hash));

	st<<_send_to_maze;
	st>>tmp;
	mp.insert(pair<string, string>("send_to_maze", tmp));
	st.clear();
	tmp.clear();

	st<<_offset;
	st>>tmp;
	mp.insert(pair<string, string>("offset", tmp));
	st.clear();
	tmp.clear();
	
	st<<_length;
	st>>tmp;
	mp.insert(pair<string, string>("length", tmp));
	st.clear();
	tmp.clear();
	st<<_sha_offset;
	st>>tmp;
	mp.insert(pair<string, string>("sha_offset", tmp));

	st.clear();
	tmp.clear();
	st<<_create_time;
	st>>tmp;
	mp.insert(pair<string, string>("create_time", tmp));
	
	st.clear();
	tmp.clear();
	st<<_last_time;
	st>>tmp;
	mp.insert(pair<string, string>("last_time", tmp));
	st.clear();
	tmp.clear();
	const char* mid = (const char*)_check;
	fs::byte2hexstr(mid, 20, tmp);
	//tmp.assign(mid, 40);
	mp.insert(pair<string, string>("check", tmp));

	return 0;
}

int meta_data::parse(map<string, string>& mp)
{
	int count = 0;
	string str;
	str = mp["file_id"];
	if (!str.empty())
	{
		++count;
		_file_id = str;
	}
	str = mp["file_name"];
	if (!str.empty())
	{
		++count;
		_file_name = str;
	}
	str = mp["taskid"];
	if (!str.empty())
	{
		++count;
		_task_id = str;
	}
	//uid
	str = mp["uid"];
	if (!str.empty())
	{
		++count;
		_uid= str;
	}
	//hashid
	str = mp["hashid"];
	if (!str.empty())
	{
		++count;
		_hash_id = str;
	}
	//uhash
	str = mp["uhash"];
	if (!str.empty())
	{
		++count;
		_uhash = str;
	}
	str = mp["key"];
	if (!str.empty())
	{
		++count;
		_key = str;
	}
	
	str = mp["offset"];
	if (!str.empty())
	{
		++count;
		_offset = atoll(str.c_str());
	}
	str = mp["length"];
	if (!str.empty())
	{
		++count;
		_length = atoll(str.c_str());
	}
	str = mp["sha_offset"];
	if (!str.empty())
	{
		++count;
		_sha_offset = atoll(str.c_str());
		_offset = _sha_offset;
	}
	str = mp["create_time"];
	if (!str.empty())
	{
		++count;
		_create_time = atoll(str.c_str());
	}
	str = mp["last_time"];
	if (!str.empty())
	{
		++count;
		_last_time = atoll(str.c_str());
	}
	str = mp["send_to_maze"];
	if ( !str.empty())
	{
		++count;
		_send_to_maze = atoi(str.c_str());
	}
	
	str = mp["check"];
	if (str.size() == 40)
	{
		/*SHA_1 sha;
		string sck;
		sha.Reset();
		sha.Update((unsigned char*)_file_id.c_str(), _file_id.size());
		sha.Update((unsigned char*)_file_name.c_str(), _file_name.size());
		//sha.Update(&_offset, 8);
		sha.Update((unsigned char*)&_length, 8);
		sha.Update((unsigned char*)&_sha_offset, 8);
		sha.Update((unsigned char*)&_last_time, 8);
		sha.Final();
		sha.GetHash(_check);
		fs::byte2hexstr((const char*)_check, 20, sck);
		if (sck == str)
		{
			++count;
		}
		*/
		
/*		//string str1;
		//char s[40] = {0};
		//fs::hexstr2byte(str.c_str(), 40, str1);
		for (int i = 0; i<40; i+=2)
		{
			char upper = 0;
			char lower = 0;
			if (fs::get_hex_char_val(str[i], upper) !=0 || fs::get_hex_char_val(str[i + 1], lower) != 0)
			{
				--count;
				break;
			}
			else
			{
				_check[i / 2] =(upper<<4) | lower;
			}
		}
		//memmove(_sha_middle, s, 40);*/
	}
	
	if (count >= 8)
	{
		return 0;
	}
	else
	{
		return -1;
	}
	
	return 0;
}

