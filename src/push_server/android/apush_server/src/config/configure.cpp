#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <math.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <iostream>
#include <sstream>
#include "json/json.h"
#include "k_configure.h"
#include "dbg.h"
#include "util.h"
#include "configure.h"

using  fs::k_configure;

configure* configure::_inst = NULL;

configure::configure()
{
}
configure::~configure() {}

configure* configure::instance()
{
	if ( _inst == NULL)
		_inst = new configure();
	return _inst;
}



int configure::start(const string& path)
{
	//read configure file
	k_configure conf;
	if ( conf.open(path.c_str()) != 0) 
	{
		DBG_ERROR("open configure file error");
		return -1;
	}

	cdata data;

	int port = 0;
	//service
	conf.get_integer_value("service","service_port",port);
	data._service_port= port;
	conf.get_integer_value("service","service_worker_num",data._service_worker_num);
	conf.get_integer_value("service","service_timeout",data._service_timeout);

	//mgmt
	conf.get_integer_value("mgmt","mgmt_port",port);
	data._mgmt_port= port;
	conf.get_integer_value("mgmt","mgmt_worker_num",data._mgmt_worker_num);
	conf.get_integer_value("mgmt","http_timeout",data._http_timeout);

    //push
    conf.get_string_value("push","app_type",data._app_type);
    //conf.get_integer_value("push","max_msg_num",data._max_msg_num);
    conf.get_integer_value("push","repush_interval",data._repush_interval);
    //
    conf.get_integer_value("push","max_qps",data._max_qps);
    conf.get_integer_value("push","push_timeout",data._push_timeout);

    //push_mgr
    string push_mgr_host;
    conf.get_string_value("visitor","push_mgr_host", push_mgr_host);
    data._push_mgr_host = push_mgr_host;
    
    string spush_mgr_ip;
    conf.get_string_value("visitor","push_mgr_ip",spush_mgr_ip);
	data._spush_mgr_ip = spush_mgr_ip;
    if (!data._spush_mgr_ip.empty()) {
        util::instance()->str2ip(data._spush_mgr_ip, data._push_mgr_ip);
    }
    
    int push_mgr_port = 0;
    conf.get_integer_value("visitor","push_mgr_port",push_mgr_port);
    data._push_mgr_port = push_mgr_port;

	//log
	conf.get_string_value("log","log_path",data._log_path);
	conf.get_string_value("log","push_server_ip",data._push_server_ip);
	conf.get_integer_value("log","cutdown_interval",data._cutdown_interval);
	//conf.get_integer_value("log","test",data._test);
    conf.get_integer_value("log","log_level",data._log_level);

    //user
    conf.get_integer_value("user","max_user_num",data._max_user_num);

    //htbt
    conf.get_integer_value("htbt","htbt_interval",data._htbt_interval);
	
	//check the configure item 
	if ( check_config(data) != 0) 
	{
		DBG_ERROR("check_config() error");
		return -1;
	}

	
	//fsk::kunique_lock<fsk::kshared_mutex> lck(_mutex);
	_path = path;
	_data = data;

	print();

	DBG_INFO("success to read configure");
	return 0;
}

int configure::check_config(const cdata& data)
{
	if(
	      data._service_port <= 0
	   || data._service_worker_num <= 0
	   || data._service_timeout <= 0
	   || data._mgmt_port <= 0
	   || data._mgmt_worker_num <= 0
	   || data._http_timeout <= 0
	   || data._max_msg_num <= 0
	   || data._repush_interval <= 0
	   || data._max_qps <= 0
	   || data._push_timeout <= 0
       || data._app_type.size() == 0
	   || data._log_buff_size <= 0
	   || data._cutdown_interval <= 0
	   || data._log_path.size() <= 0
       || data._log_level < 0
	   || data._push_server_ip.size() <= 0
       || data._push_mgr_port <= 0
       || data._max_user_num <= 0
       || data._htbt_interval <= 0
       || (data._push_mgr_host.empty() && data._spush_mgr_ip.empty())
	   ) 
	{
		DBG_ERROR("configure error may be some parameters <= 0");
		return -1;
	}
	return 0;
}

unsigned short configure::get_service_port() 
{	
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._service_port;
}

int configure::get_service_worker_num() 
{	
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._service_worker_num;
}

int configure::get_service_timeout() 
{	
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._service_timeout;
}

unsigned short configure::get_mgmt_port()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._mgmt_port;
}

int configure::get_mgmt_worker_num()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._mgmt_worker_num;
}

int configure::get_http_timeout()
{
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._http_timeout;
}

string configure::get_app_type()
{
    return _data._app_type;
}

int configure::get_max_msg_num()
{
    return _data._max_msg_num;
}

int configure::get_repush_interval()
{
    return _data._repush_interval;
}

int configure::get_max_qps()
{
    return _data._max_qps;
}

int configure::get_push_timeout()
{
    return _data._push_timeout;
}

int configure::get_log_buff_size()
{
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._log_buff_size;
}

int configure::get_cutdown_interval()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._cutdown_interval;
}

int configure::get_test()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._test;
}


int configure::get_log_level()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._log_level;
}

string configure::get_log_path()
{
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._log_path;
}

string configure::get_push_server_ip()
{
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return _data._push_server_ip;
}

unsigned int configure::get_push_mgr_ip()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    unsigned int ip = _data._push_mgr_ip;
    if (!_data._push_mgr_host.empty()) {
        struct hostent *hptr = NULL;
        hptr = gethostbyname(_data._push_mgr_host.c_str());
        if(hptr != NULL) {
            char ip_str[32] = {0};
            inet_ntop(hptr->h_addrtype, hptr->h_addr_list[0], ip_str, sizeof(ip_str));
            util::instance()->str2ip(ip_str, ip);
        }
    } 
    return ip;
}

string configure::get_spush_mgr_ip()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._spush_mgr_ip;
}

string configure::get_push_mgr_host()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._push_mgr_host;
}

unsigned short configure::get_push_mgr_port()
{
    //fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
    return _data._push_mgr_port;
}

int configure::get_max_user_num()
{
    return _data._max_user_num;
}

int configure::get_htbt_interval()
{
    return _data._htbt_interval;
}

string configure::get_server_version()
{
	//fsk::kshared_lock<fsk::kshared_mutex> lck(_mutex);
	return APUSH_SERVER_VERSION;
}

int configure::printn(unsigned char *pkt,int len)
{
    cout<<endl;
    for(int i=0;i<len;i++)
    {
        printf("%x,",pkt[i]);
    }
    cout<<endl;
    return 0;
}

int configure::print()
{
	cout<<"\n=========================configure file=========================\n";
	cout<<"service_port="<<_data._service_port<<endl;
	cout<<"service_worker_num="<<_data._service_worker_num<<endl;
	cout<<"service_timeout="<<_data._service_timeout<<endl;
	cout<<"mgmt_port="<<_data._mgmt_port<<endl;
	cout<<"mgmt_worker_num="<<_data._mgmt_worker_num<<endl;
	cout<<"http_timeout="<<_data._http_timeout<<endl;
	cout<<"max_msg_num="<<_data._max_msg_num<<endl;
	cout<<"http_timeout="<<_data._http_timeout<<endl;
	cout<<"repush_interval="<<_data._repush_interval<<endl;
    cout<<"app_type="<<_data._app_type<<endl;
	cout<<"cutdown_interval="<<_data._cutdown_interval<<endl;
	cout<<"max_qps="<<_data._max_qps<<endl;
	cout<<"push_timeout="<<_data._push_timeout<<endl;
	cout<<"log_path="<<_data._log_path.data()<<endl;
	cout<<"log_level"<<_data._log_level<<endl;
	cout<<"push_mgr_ip="<<_data._spush_mgr_ip.data()<<endl;
	cout<<"push_mgr_port="<<_data._push_mgr_port<<endl;
    cout<<"max_user_num="<<_data._max_user_num<<endl;
	cout<<"\n=========================configure file=========================\n";
	
	return 0;
}



