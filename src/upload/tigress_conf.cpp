#include <arpa/inet.h>
#include <fstream>
#include "tigress_conf.h"

tigress_conf* tigress_conf::_instance = new tigress_conf();

tigress_conf::tigress_conf()
{
	 _conf = new fs::k_configure();
	 _conf_default = new fs::k_configure();
}

tigress_conf::~tigress_conf()
{

}

tigress_conf* tigress_conf::get_instance()
{
	if (NULL == _instance)
	{
		_instance = new tigress_conf();
	}

	return _instance;
}

int tigress_conf::open(const char* file_path, const char* file_path_default)
{
	int ret = 0;

	ret |= _conf->open(file_path);
	ret |= _conf_default->open(file_path_default);

	string tmp ;
	//maze info
	_conf->get_string_value("visitor","maze_ip",tmp);
	unsigned int ip = 0;
	if ( str2ip(tmp,ip) != 0)
	{
		cout<<"maze_ip error"<<endl;
	}
	_mconf.insert(make_pair("maze_ip",ip));
	
	_conf->get_string_value("visitor","maze_port",tmp);
	//unsigned short port = htons(atoi(tmp.data()));
	unsigned short port = atoi(tmp.data());
	_mconf.insert(make_pair("maze_port",port));

	//trnacecode info
	_conf->get_string_value("visitor","transcode_ip",tmp);
	ip = 0;
	if ( str2ip(tmp,ip) != 0)
	{
		cout<<"trancecode_ip error"<<endl;
	}
	_mconf.insert(make_pair("transcode_ip",ip));
	
	_conf->get_string_value("visitor","transcode_port",tmp);
	 //port = htons(atoi(tmp.data()));
	 port = atoi(tmp.data());
	_mconf.insert(make_pair("transcode_port",port));

	//local_host_ip info
	_conf->get_string_value("visitor","local_host_ip",tmp);
	ip = 0;
	if ( str2ip(tmp,ip) != 0)
	{
		cout<<"local_host_ip error"<<endl;
	}
	_mconf.insert(make_pair("local_host_ip",ip));

	load_xml_data();

	return ret;
}

int tigress_conf::load_xml_data()
{
	_xml_data.clear();
	ifstream fin("./etc/crossdomain.xml");
	string str;

	char arr[4096];
	if(!fin.eof())
	{
		fin.read(arr,4095);
		int num = fin.gcount();
		 _xml_data.assign(arr,num);
	}
}

int tigress_conf::get_integer_value(const char* section_name, const char* option_name, int& value)
{
	if (0 != _conf->get_integer_value(section_name, option_name, value))
	{
		return _conf_default->get_integer_value(section_name, option_name, value);
		//return get_default_integer(section_name, option_name, value);
	}
	else
	{
		return 0;
	}
}

int tigress_conf::get_string_value(const char* section_name, const char* option_name, string& value)
{
	if (0 != _conf->get_string_value(section_name, option_name, value))
	{
		return _conf_default->get_string_value(section_name, option_name, value);
		//return get_default_string(section_name, option_name, value);
	}
	else
	{
		return 0;
	}
}


int tigress_conf::get_float_value(const char* section_name, const char* option_name, float& value)
{
	if (0 != _conf->get_float_value(section_name, option_name, value))
	{
		return _conf_default->get_float_value(section_name, option_name, value);
		//return get_default_string(section_name, option_name, value);
	}
	else
	{
		return 0;
	}
}

unsigned int tigress_conf::get_int_value(string name)
{
	map<string,unsigned int>::iterator iter = _mconf.find(name);
	if ( iter != _mconf.end())
	{
		return iter->second;
	}

	return 0;
}

int tigress_conf::str2ip(const string& str,unsigned int& ip)
{
	in_addr ipaddr;
	memset(&ipaddr,0,sizeof(ipaddr));
	if ( inet_pton(AF_INET,str.c_str(),(struct in_addr*)&ipaddr) > 0) 
	{
		ip = ntohl(ipaddr.s_addr);
		//ip = ipaddr.s_addr;
		return 0;
	}
	return -1;
}

string tigress_conf::get_xml_data()
{
	return _xml_data;
}


