#include "task_timer.h"
#include "flush_log.h"
#include "task_aging.h"
#include "task_report_push.h" 
#include "update_user_num.h"
#include "configure.h"
#include "dbg.h"

task_timer::task_timer()
{
}

task_timer::~task_timer()
{
}

task_timer* task_timer::_inst = NULL;
task_timer* task_timer::instance()
{
	if(_inst == NULL)
		_inst = new task_timer();
	return _inst;
}

int task_timer::start()
{
	fsk::ktimer<fsk::ktimer_list> * ptimer = new fsk::ktimer<fsk::ktimer_list>;
	ptimer->initialize();
	
	ptimer->schedule(new flush_log(), fsk::ktimeval(1, 0), fsk::ktimeval(configure::instance()->get_cutdown_interval(), 0)); 
	ptimer->schedule(new task_aging(), fsk::ktimeval(1, 0), fsk::ktimeval(10, 0)); 
	ptimer->schedule(new task_report_push(), fsk::ktimeval(1, 0), fsk::ktimeval(10, 0)); 
	ptimer->schedule(new update_user_num(), fsk::ktimeval(1, 0), fsk::ktimeval(10, 0)); 
	
	return 0;
}


