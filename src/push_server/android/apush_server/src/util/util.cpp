#include <string.h>
#include <sys/time.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <iostream>
#include "http_response.h"
#include "dbg.h"
#include "json/json.h"
#include "util.h"

using namespace std;
using  fs::http_response;

util* util::_inst = NULL;
util* util::instance()
{
	if ( _inst == NULL)
		_inst = new util();
	return _inst;
}

util::util()
{
    /*
    Json::Value tmp_value;
    tmp_value["error"] = "1";
    _err_resp = tmp_value.toStyledString();


    Json::Value ok_value;
    ok_value["error"] = "0";
    _ok_resp = ok_value.toStyledString();
    */

    _err_resp = "{\"error\":\"1\"}";
    _ok_resp = "{\"error\":\"0\"}";


    
    string err_msg = "{\"retcode\":\"400\"}";

    http_response http_resp_400;
    http_resp_400._resp._content = err_msg;
    if (http_resp_400.pack(_http_400_resp) < 0)
    {
        DBG_ERROR("pack 400 resp error");
    }
    
    http_response http_resp_403;
    err_msg = "{\"retcode\":\"403\"}";
    http_resp_403._resp._content = err_msg;
    if (http_resp_403.pack(_http_403_resp) < 0)
    {
        DBG_ERROR("pack 403 resp error");
    }
    http_response http_resp_404;
    err_msg = "{\"retcode\":\"404\"}";
    http_resp_404._resp._content = err_msg;
    if (http_resp_404.pack(_http_404_resp) < 0)
    {
        DBG_ERROR("pack 404 resp error");
    }   
 
    http_response http_resp_408;
    err_msg = "{\"retcode\":\"408\"}";
    http_resp_408._resp._content = err_msg;
    if (http_resp_408.pack(_http_408_resp) < 0)
    {
        DBG_ERROR("pack 408 resp error");
    }

    http_response http_resp_200;
    err_msg = "{\"retcode\":\"200\"}";
    http_resp_200._resp._content = err_msg;
    if (http_resp_200.pack(_http_200_resp) < 0)
    {
        DBG_ERROR("pack 200 resp error");
    }
    
}

int util::get_app_id(string& appname)
{
    int res = -1;
    map<string,int>::iterator iter = _app_type.find(appname);
    if ( iter != _app_type.end())
    {
        res = iter->second;
    }

    return res;
}

string util::get_app_name(int appid)
{
    string app_name;
    map<int,string>::iterator iter = _rapp_type.find(appid);
    if ( iter != _rapp_type.end())
    {
       app_name = iter->second;
    }

    return app_name;
}

int util::get_app_list(map<int,string>& appid_list)
{
    appid_list = _rapp_type;
    return 0;
}

int util::set_app_type(string apptype)
{
    int res = -1;
    Json::Reader reader(Json::Features::strictMode());
    Json::Value value;
    string key = "android";
    if ( reader.parse(apptype,value))
    {
        Json::Value value1;
        value1 = value[key];
        int size = value1.size();
        for ( int i=0;i<size;i++)
        {
            string tmp = value1[i].asString();
            _app_type.insert(make_pair(tmp,i));
            _rapp_type.insert(make_pair(i,tmp));
        }
    }
    else
    {
        return -1;
    }

    if ( _app_type.size() == 0)
    {
       return  -1;
    }
    
    return 0;
}

string util::get_error_resp()
{
    return _err_resp;
}

string util::get_ok_resp()
{
    return _ok_resp;
}

string util::get_http_400_resp()
{
    return _http_400_resp;
}
string util::get_http_403_resp()
{
    return _http_403_resp;
}
string util::get_http_404_resp()
{
    return _http_404_resp;
}
string util::get_http_408_resp()
{
    return _http_408_resp;
}

string util::get_http_200_resp()
{
    return _http_200_resp;
}

int util::ip2str(const unsigned int & ip,string& ipstr)
{
	struct in_addr ip_addr;
	memset(&ip_addr,0,sizeof(in_addr));
	ip_addr.s_addr = ip;
	char ipbuf[INET_ADDRSTRLEN]= {0};
	if ( inet_ntop(AF_INET,(struct in_addr*)&ip_addr,ipbuf,INET_ADDRSTRLEN)!= NULL) 
	{
		ipstr = string(ipbuf,strlen(ipbuf));
		return 0;
	}
	return -1;
}

int util::str2ip(const string& str,unsigned int& ip)
{
	in_addr ipaddr;
	memset(&ipaddr,0,sizeof(ipaddr));
	if ( inet_pton(AF_INET,str.c_str(),(struct in_addr*)&ipaddr) > 0) 
	{
		ip = ntohl(ipaddr.s_addr);
		return 0;
	}
	return -1;
}

bool util::is_sleepping_time()
{
    time_t now = time(NULL);
    struct tm* local_time = localtime(&now);
    int hour = local_time->tm_hour;
    if (hour >= 23 || (hour >=0 && hour <= 8)) {
        return true;
    }
    return false;
}

/*
*	decode escape string (like %AB%0D%....) to strings
*@param str	input string to decode
*@param len	length of the str
*@res	out, decode result
*return:
*	0, always success
*/
int util::escape2str(const char * str, int len, string &res)
{
	int i=0;
	int pos = 0;
	char buf[65535] = {0};
	while(i < len)
	{
		char c = *(str+i);
		if(c != '%')
		{
			*(buf+pos) = c;
			pos++;
			i++;
		}
		else
		{
			if(i < len-2)
			{
				i++;
				c = *(str+i);

				if(c>='0' && c<='9')
					*(buf+pos) |= ((c-'0')<<4);
				else if(c>='a' && c<='f')
					*(buf+pos) |= ((c-'a'+10)<<4);
				else if(c>='A' && c<='F')
					*(buf+pos) |= ((c-'A'+10)<<4);
				else
					break;

				i++;
				c = *(str+i);
				if(c>='0' && c<='9')
					*(buf+pos) |= ((c-'0'));
				else if(c>='a' && c<='f')
					*(buf+pos) |= ((c-'a'+10));
				else if(c>='A' && c<='F')
					*(buf+pos) |= ((c-'A'+10));
				else
					break;

				pos++;
				i++;
			}
			else
				break;
		}
	}

	res.assign(buf, pos);
	return 0;
}

string util::get_time() 
{
    char buf[64];
    memset(buf, 0, sizeof(buf));

    time_t t = time(0);
    strftime(buf, sizeof(buf), "%Y/%m/%d %H:%M:%S", localtime(&t));

    return string(buf);
}

unsigned long long util::get_conn_id(int thread_index, int id)
{
    return ((unsigned long long)thread_index << 32) | id;
}
