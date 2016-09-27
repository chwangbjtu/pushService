#include <arpa/inet.h>
#include <string.h>
#include <sstream>
#include "json/json.h"
#include "configure.h"
#include "proto_constant.h"
#include "proto_process.h"

string proto_login::_resp = "";
string proto_htbt::_resp = "";

proto_login::proto_login()
{
    /*
    _resp.assign(sizeof(header_struct_t),'\0');
    header_struct_t * presp = (header_struct_t *)(_resp.data());

    presp->_version = htons(version1);
    presp->_type = htons(proto_login_resp);
    //presp->_magic_code = 0;
    presp->_length = 0;
    */

    Json::Value titem;
    string shtbt;
    //shtbt.assign(itoa(configure::instance()->get_htbt_interval()));
    stringstream ss;
    ss<<configure::instance()->get_htbt_interval();
    shtbt = ss.str();
    titem["htbt"] = shtbt;
    string sresp;
    sresp = titem.toStyledString();

    _resp.assign(sizeof(header_struct_t),'\0');
    
    header_struct_t * presp = (header_struct_t *)(_resp.data());
    //presp->_a_index = 1;

    presp->_version = htons(version1);
    presp->_type = htons(proto_login_resp);
    //presp->_magic_code = 0;
    presp->_length = htonl(sresp.size()+proto_header_len);
    _resp.append(sresp);
}

int proto_login::pack_resp_v1(string& resp)
{
    header_struct_t * presp = (header_struct_t *)(_resp.data());
    //presp->_random = rand();
    //resp = _resp;
    resp.assign(_resp.size(),'\0');
    memcpy((void *)resp.data(),(void *)_resp.data(),_resp.size());
    return 0;
}

proto_htbt::proto_htbt()
{
    _resp.assign(sizeof(header_struct_t),'\0');
    header_struct_t * presp = (header_struct_t *)(_resp.data());

    presp->_version = htons(version1);
    presp->_type = htons(proto_htbt_resp);
    //presp->_magic_code = 0;
    presp->_length = htonl(proto_header_len);
}

int proto_htbt::pack_resp_v1(string& resp)
{
    //resp = _resp;
    resp.assign(_resp.size(),'\0');
    memcpy((void*)resp.data(),(void*)_resp.data(),_resp.size());
    return 0;
}


int proto_push::pack_push_v1(list<string>& msginfo_list,string& resp)
{
    if (msginfo_list.empty())
        return 0;

	list<string>::iterator iter = msginfo_list.begin();
	for ( ; iter!= msginfo_list.end();iter++)
	{
		string tresp;
		pack_push_v1(*iter,tresp);
		resp.append(tresp);
	}

    return 0;
}

int proto_push::pack_push_v1(string& msg,string& resp)
{
    if (msg.size() == 0)
        return 0;

    resp.assign(sizeof(header_struct_t),'\0');
    header_struct_t * presp = (header_struct_t *)(resp.data());

    presp->_version = htons(version1);
    presp->_type = htons(proto_push_resp);
    //presp->_magic_code = 0;
    presp->_length = htonl(msg.size()+proto_header_len);

    resp.append(msg);

    return 0;
}
