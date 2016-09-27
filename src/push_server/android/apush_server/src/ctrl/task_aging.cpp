#include "task_aging.h"
#include "dbg.h"
#include "msg_mgr.h"
#include "msg_cnt_mgr.h"


task_aging::task_aging():_cnt(1)
{
}

task_aging::~task_aging() 
{
}


int task_aging::run(const time_t now)
{
    //msg_mgr::instance()->aging();
    msg_cnt_mgr::instance()->aging();

	return 0;
}



