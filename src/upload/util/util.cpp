#include <iostream>
#include "util.h"

using namespace std;

util* util::_inst = NULL;
util* util::instance()
{
	if ( _inst == NULL)
		_inst = new util();
	return _inst;
}

util::util()
{
}

string util::get_key(const string& taskid)
{
	return "boa4poz1";
}


