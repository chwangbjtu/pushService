#ifndef __CONFIGURE_H
#define __CONFIGURE_H
#include <string>
#include <map>
#include <vector>
#include "kmutex.h"
#include "klock.h"

using namespace std;

#define APUSH_SERVER_VERSION "0.1.0.01"

//configure item
class cdata
{
public:
	cdata():
		_service_port(8080),
		_service_worker_num(4),
		_service_timeout(1000),
		_mgmt_port(8010),
		_mgmt_worker_num(2),
		_http_timeout(20),
        _max_msg_num(4),
        _repush_interval(10),
		_log_buff_size(1024*50),
	    _cutdown_interval(300),
        _test(0),
        _log_level(-1),
		_push_mgr_ip(0),
		_push_mgr_port(0),
        _max_user_num(2000000),
        _htbt_interval(120),
        _max_qps(10000),
        _push_timeout(3600)
	{
		_log_path = "./log/";
		_push_server_ip = "127.0.0.1";
	}

	unsigned short _service_port;
	int _service_worker_num;
	int _service_timeout;

	unsigned short _mgmt_port;
	int _mgmt_worker_num;
	int _http_timeout;

	int _log_buff_size;
	int _cutdown_interval;
	string _log_path;
	string _push_server_ip;
    int _test;
    //trace:0,debug:1,info:2,warn:3,error:4,fatal:5
    int _log_level;

    string _push_mgr_host;
    unsigned int _push_mgr_ip;
    unsigned short _push_mgr_port;
    string _spush_mgr_ip;

    int _max_user_num;

    int _htbt_interval;

    string _app_type;
    int _max_msg_num;
    int _repush_interval;
    int _push_timeout;
    //每秒向多少客户端推送消息
    int _max_qps;
};


/*
 *read configure at  10s interval and check each item.if error found,exit this
 * programme.
 * */
class configure
{
public:
	~configure();
	static configure* instance();
	/* read configure file
	 *@para[in]file:filename of configure name
	 *@return:
	 *  0:success,-1:failed
	 **/
	int start(const string& file);

	//getter 
	unsigned short get_service_port() ;
	int get_service_worker_num();
	int get_service_timeout();
	
	unsigned short get_mgmt_port() ;
	int get_mgmt_worker_num();
	int get_http_timeout();

	int get_log_buff_size();
	string get_push_server_ip();
	string get_log_path();
	int get_cutdown_interval();
    int get_test();
    int get_log_level();

    unsigned int get_push_mgr_ip();
    unsigned short get_push_mgr_port();
    string get_spush_mgr_ip();
    string get_push_mgr_host();

    int get_max_user_num();

    int get_htbt_interval();

    string get_app_type();
    int get_max_msg_num();
    int get_repush_interval();
    int get_max_qps();
    int get_push_timeout();

	int print();
    int printn(unsigned char *pkt,int len);

	string get_server_version();

private:
	configure();
	/* check the  validity of each item in configure file
	 * @para[in]d: configure file item 
	 * @return:
	 *  0:success,-1: error item existed in configure file
	 * */
	int check_config(const cdata& data);
	
	int str2ip(const string& str,unsigned int& ip);
private:
	string _path;
	cdata _data;
	static configure* _inst;
	fsk::kshared_mutex _mutex;
};

#endif//__CONFIGURE_H

