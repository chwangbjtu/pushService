#ifndef __FP_BASE_HANDLER_H
#define __FP_BASE_HANDLER_H
#include <string>
#include <map>


using namespace std;
class fp_base_handler
{
public:
	fp_base_handler();
	
	//virtual int process(const multimap<string,string>& req,unsigned int ip,string& resp){return -1;}
	virtual int process(string& req,unsigned int ip,int threadid,int& id,string& rtoken,string& resp){return -1;}
	
	virtual ~fp_base_handler(){};
protected:

	int pack(string& msg,string& resp);
};

#endif //__FP_BASE_HANDLER_H

