
#ifndef __TIGRESS_CONF__
#define __TIGRESS_CONF__

#include <iostream>
#include <map>
#include <string>
#include "k_configure.h"

using namespace std;

class tigress_conf
{
	public:
		~tigress_conf();
		static tigress_conf* get_instance();
		int open(const char* file_path, const char* file_path_default);
		int get_integer_value(const char* section_name, const char* option_name, int& value);
		int get_string_value(const char* section_name, const char* option_name, string& value);
		int get_float_value(const char* section_name, const char* option_name, float &value);
		//int set_default_integer(const string& section_name,const string& option_name,int value);
		//int set_default_string(const string& section_name,const string& option_name,string& value);
		//int get_default_integer(const string& section_name,const string& option_name,int& value);
		//int get_default_string(const string& section_name,const string& option_name,string& value);

		unsigned int get_int_value(string name);

		int str2ip(const string& str,unsigned int& ip);

		string get_xml_data();
	private:
		int load_xml_data();

	private:
		tigress_conf();
		static tigress_conf* _instance;

		fs::k_configure* _conf;
		fs::k_configure* _conf_default;
		map<string,unsigned int> _mconf;
		string _xml_data;
		//map<string, map<string, string> > _str;
		//map<string, map<string, int> > _int;
};

#endif
