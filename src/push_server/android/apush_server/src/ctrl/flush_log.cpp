#include "flush_log.h"
#include "tlogger.h"
#include "dbg.h"
#include "configure.h"


flush_log::flush_log():_cnt(1)
{
}

flush_log::~flush_log() 
{
}


int flush_log::run(const time_t now)
{
    tlogger::instance()->flush();
	return 0;
}



