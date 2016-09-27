#include<iostream>
#include<sstream>
#include <arpa/inet.h>
#include <netdb.h>
#include<sstream>

#include "writer_file.h"
#include "filter_level.h"
#include "writer_console.h"
#include "layout_pattern.h"
#include "writer_buffered.h"
	
#include "k_str.h"
#include "dbg.h"
#include "util.h"
#include "configure.h"
#include "tlogger.h"


using namespace std;
tlogger * tlogger::_inst = NULL;
tlogger * tlogger::instance ()
{
	if (_inst == NULL)
		_inst = new tlogger ();
	return _inst;
}

tlogger::tlogger ()
{
}

int tlogger::flush()
{
	boost::mutex::scoped_lock lock(_mutex);
	_tlog->flush();
	_mtlog->flush();
	return 0;
}


int tlogger::mlog(fsk::levelptr_t level, const char* fmt, ...)
{
    boost::mutex::scoped_lock lock(_mutex);

    char buffer[MAX_LOGMSG_SIZE] = {0};
    va_list va;
    string format = "[" + util::get_time() + "] " + string(fmt);
    va_start(va, fmt);
    vsnprintf(buffer, MAX_LOGMSG_SIZE - 1, format.c_str(), va);
    va_end(va);

    fsk::logitem_t item(buffer, level);
    _mtlog ->log(&item);

}

//int tlogger::log(string filename,int line,fsk::levelptr_t level,string info)
int tlogger::mlog(string& module,fsk::levelptr_t level,string info)
{
	boost::mutex::scoped_lock lock(_mutex);
	std::stringstream ss;
	ss<<module<<" "
        <<time(NULL)<<" "
        <<level->name()<<" "
        <<info;
	string tinfo = ss.str();

    fsk::logitem_t item(tinfo, level);
    _mtlog->log(&item);
	//_tlog->log("%s\n",tinfo.data());
	return 0;
}

int tlogger::mlog(string module,fsk::levelptr_t level,int errno1)
{
    boost::mutex::scoped_lock lock(_mutex);
    std::stringstream ss;
    ss<<module<<" "
        <<time(NULL)<<" "
        <<level->name()<<" "
        <<errno1;
    string tinfo = ss.str();

    fsk::logitem_t item(tinfo, level);
    _mtlog->log(&item);
    return 0;
}

int  tlogger::log(string module,fsk::levelptr_t level,std::string& fudid,unsigned int area,unsigned version,int in)//in,in:1 or out:0
{
    string sip;
    string sver;
    util::instance()->ip2str(htonl(area),sip);
    util::instance()->ip2str(htonl(version),sver);
    
    boost::mutex::scoped_lock lock(_mutex);
    std::stringstream ss;
    ss<<module<<" "
        <<time(NULL)<<" "
        <<level->name()<<" "
        <<fudid<<" "
        <<sip<<","
        <<sver<<" "
        <<in;

    string tinfo = ss.str();
    
    fsk::logitem_t item(tinfo, level);
    _tlog->log(&item);

    return 0;
}

int  tlogger::log(string module,fsk::levelptr_t level,std::string& fudid,int msgid,int in)//in,in:1 or out:0
{
    boost::mutex::scoped_lock lock(_mutex);
    std::stringstream ss;
    ss<<module<<" "
        <<time(NULL)<<" "
        <<level->name()<<" "
        <<fudid<<" "
        <<msgid<<" "
        <<in;

    string tinfo = ss.str();

    fsk::logitem_t item(tinfo, level);
    _tlog->log(&item);

    return 0;
}

int  tlogger::log(string module,fsk::levelptr_t level,std::string& fudid,string& info,int in)//in,in:1 or out:0
{
    boost::mutex::scoped_lock lock(_mutex);
    std::stringstream ss;
    ss<<module<<" "
        <<time(NULL)<<" "
        <<level->name()<<" "
        <<fudid<<" "
        <<info<<" "
        <<in;

    string tinfo = ss.str();

    fsk::logitem_t item(tinfo, level);
    _tlog->log(&item);

    return 0;
}

int tlogger::start()
{
	int log_size_mb = 50;
    string log_path = configure::instance()->get_log_path();
	_tlog = new fsk::time_cycled_logger("apushserver_%Y%m%d.log",fsk::LDAY, new fsk::writer_file(log_path));
	if (!_tlog)
	{
		cout<<"NULL POINTER _wtr or _log"<<endl;
		return -1;
	}

    /////////////
    _mtlog = new fsk::time_cycled_logger("monitor_apushserver_%Y%m%d.log",fsk::LDAY, new fsk::writer_file(log_path));
    if (!_mtlog)
    {
        cout<<"NULL POINTER _wtr or _log ,monitor"<<endl;
        return -1;
    }

    //trace:0,debug:1,info:2,warn:3,error:4,fatal:5
    int log_level = configure::instance()->get_log_level();
    if ( log_level == 0)
    {
        _tlog->set_filter(new fsk::filter_level(fsk::level_t::trace_level()));
        _mtlog->set_filter(new fsk::filter_level(fsk::level_t::trace_level()));
    }
    else if ( log_level == 1)
    {
        _tlog->set_filter(new fsk::filter_level(fsk::level_t::debug_level()));
        _mtlog->set_filter(new fsk::filter_level(fsk::level_t::debug_level()));
    }
    else if( log_level == 2)
    {
        _tlog->set_filter(new fsk::filter_level(fsk::level_t::info_level()));
        _mtlog->set_filter(new fsk::filter_level(fsk::level_t::info_level()));
    }
    else if( log_level == 3)
    {
        _tlog->set_filter(new fsk::filter_level(fsk::level_t::warn_level()));
        _mtlog->set_filter(new fsk::filter_level(fsk::level_t::warn_level()));
    }
    else if( log_level == 4)
    {
        _tlog->set_filter(new fsk::filter_level(fsk::level_t::error_level()));
        _mtlog->set_filter(new fsk::filter_level(fsk::level_t::error_level()));
    }
    else if( log_level == 5)
    {
        _tlog->set_filter(new fsk::filter_level(fsk::level_t::fatal_level()));
        _mtlog->set_filter(new fsk::filter_level(fsk::level_t::fatal_level()));
    }

	//_tlog->set_layout(new fsk::layout_pattern("[%t][%T][%l] %m [%L]\r\n"));
	_tlog->set_layout(new fsk::layout_pattern("%m\r\n"));
	_tlog->open();


    //_mtlog->set_layout(new fsk::layout_pattern("[%t][%T][%l] %m [%L]\r\n"));
    _mtlog->set_layout(new fsk::layout_pattern("%m\r\n"));
    _mtlog->open();

	
	return 0;
}



