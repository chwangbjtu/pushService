#ifndef __UTIL_H
#define __UTIL_H

using namespace std;

class util
{
public:
	~util(){}
	
	static util* instance();

	string get_key(const string& taskid);
	
private:
	util();
	static util* _inst;
};

#endif//__UTIL_H


