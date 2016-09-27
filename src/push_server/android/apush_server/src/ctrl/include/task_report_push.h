#ifndef __TASK_REPORT_PUSH_H
#define __TASK_REPORT_PUSH_H
#include "ktask.h"
#include <string>

using namespace std;

class task_report_push : public fsk::ktask	
{
public:
	task_report_push();
	~task_report_push();
	virtual int run(const time_t now);
    int pack_http_resp(std::string&, std::string&);
    int parse_key(long long key,int& appid,int& msgid);
private:
	unsigned int _cnt;
};

#endif //__TASK_REPORT_PUSH_H

