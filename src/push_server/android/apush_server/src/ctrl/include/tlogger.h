#ifndef __TLOGGER_H
#define __TLOGGER_H
#include <string>
#include <boost/thread.hpp>

#include "los.h"
#include "logger.h"
#include "filter_level.h"
#include "writer_file.h"
#include "layout_pattern.h"
#include "writer_buffered.h"
#include "size_cycled_logger.h"
#include "time_cycled_logger.h"


class tlogger
{
public:
	static tlogger* instance();
	
    int mlog(fsk::levelptr_t level, const char* fmt, ...);
    int mlog(std::string& module,fsk::levelptr_t level,std::string info);
    int mlog(std::string module,fsk::levelptr_t level,int errno1);
    int log(std::string module,fsk::levelptr_t level,std::string& fudid,unsigned int area,unsigned version,int in);
    int log(std::string module,fsk::levelptr_t level,std::string& fudid,int msgid,int in);
    int log(std::string module,fsk::levelptr_t level,std::string& fudid,std::string& info,int in);

	int flush();
	
	int start();
	
	//int stop();
	
	//void operator()();
private:
	tlogger();
	static tlogger* _inst;
	//day of this year
	time_t  _last_time;
	fsk::writer *	_wtr;
	fsk::logger* _tlog;

	fsk::writer *	_mwtr;
	fsk::logger* _mtlog;

	boost::mutex _mutex;
};
#endif //__TLOGGER_H

