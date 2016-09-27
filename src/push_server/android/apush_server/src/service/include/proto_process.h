#ifndef __PROTO_PROCESS_H
#define __PROTO_PROCESS_H
#include <list>
#include <string>
#include "proto_struct.h"

using namespace std;

class proto_login
{
public:
    proto_login();
    virtual ~proto_login() {}
    static string _resp;
    static int pack_resp_v1(string& resp);
};

class proto_htbt
{
public:
    proto_htbt();
    virtual ~proto_htbt() {}
    static string _resp;
    static int pack_resp_v1(string& resp);
};

class proto_push
{
public:
    proto_push() {}
    virtual ~proto_push() {}
	static int pack_push_v1(list<string>& msginfo_list,string& resp);
    static int pack_push_v1(string& info,string& resp);
};


#endif//__PROTO_PROCESS_H


