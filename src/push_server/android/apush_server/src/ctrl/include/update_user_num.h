#ifndef __UPDATE_USER_NUM_H
#define __UPDATE_USER_NUM_H
#include "ktask.h"

class update_user_num : public fsk::ktask	
{
public:
	update_user_num();
	~update_user_num();
	virtual int run(const time_t now);
private:
	unsigned int _cnt;
};

#endif //__UPDATE_USER_NUM_H

