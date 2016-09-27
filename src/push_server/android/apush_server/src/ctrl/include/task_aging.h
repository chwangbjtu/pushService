#ifndef __TASK_AGING_H
#define __TASK_AGING_H
#include "ktask.h"

class task_aging : public fsk::ktask	
{
public:
	task_aging();
	~task_aging();
	virtual int run(const time_t now);
private:
	unsigned int _cnt;
};

#endif //__TASK_AGING_H

