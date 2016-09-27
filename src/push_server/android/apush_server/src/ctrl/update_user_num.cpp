#include "update_user_num.h"
#include "dbg.h"
#include "user_mgr.h"


update_user_num::update_user_num():_cnt(1)
{
}

update_user_num::~update_user_num() 
{
}


int update_user_num::run(const time_t now)
{
    int max_num = 0 ;
    int remain_num = 0;
    user_mgr::instance()->get_remain_num(max_num,remain_num);
	return 0;
}



