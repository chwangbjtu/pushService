#ifndef __UTIL_H
#define __UTIL_H

#include <iostream>
#include <map>

using namespace std;

class util
{
public:
	~util(){}
	
	static util* instance();

	string get_error_resp();

    string get_ok_resp();

    string get_http_400_resp();
    string get_http_403_resp();
    string get_http_404_resp();
    string get_http_408_resp();
    string get_http_200_resp();

	int escape2str(const char * str, int len, string &res);

	int ip2str(const unsigned int & ip,string& ipstr);
	int str2ip(const string& str,unsigned int& ip);

    int get_app_id(string& appname);
    string get_app_name(int appid);
    int get_app_list(map<int,string>& appid_list);
    
    int set_app_type(string apptype);

    static string get_time();
    static bool is_sleepping_time();
    static unsigned long long get_conn_id(int thread_index, int id);
	
private:

    map<string,int> _app_type;
    map<int,string> _rapp_type;
	util();
	static util* _inst;
	char * HEX_STR;
    string _err_resp;
    string _ok_resp;

    string _http_400_resp;
    string _http_403_resp;
    string _http_404_resp;
    string _http_408_resp;
    string _http_200_resp;
};

#endif//__UTIL_H



