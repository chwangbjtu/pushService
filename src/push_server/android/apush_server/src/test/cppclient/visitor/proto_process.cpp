#include <arpa/inet.h>
#include "proto_constant.h"
#include "proto_process.h"

string proto_login::_resp = "";
string proto_htbt::_resp = "";

proto_login::proto_login()
{
    _resp.assign(sizeof(header_struct_t),'\0');
    header_struct_t * presp = (header_struct_t *)(_resp.data());

    presp->_version = htons(version1);
    presp->_type = htons(proto_login_resp);
    //presp->_magic_code = 0;
    presp->_length = 0;
}

int proto_login::pack_resp_v1(string& resp)
{
    resp = _resp;
    return 0;
}

proto_htbt::proto_htbt()
{
    _resp.assign(sizeof(header_struct_t),'\0');
    header_struct_t * presp = (header_struct_t *)(_resp.data());

    presp->_version = htons(version1);
    presp->_type = htons(proto_htbt_resp);
    //presp->_magic_code = 0;
    presp->_length = 0;
}

int proto_htbt::pack_resp_v1(string& resp)
{
    resp = _resp;
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
    presp->_length = htonl(msg.size());

    resp.append(msg);

    return 0;
}
