#ifndef __PROTO_CONSTANT_H
#define __PROTO_CONSTANT_H

#include <iostream>
#include <string>

using namespace std;


const int proto_header_len = 16;
const int proto_header_type_offset = 8;
const int proto_header_version_offset = 10;
//const int proto_header_mcode_offset = 4;
const int proto_header_length_offset = 4;
const int proto_header_max_length = 65535;
const int proto_msgid_len = 4;

//protocol type
typedef enum proto_type
{
    proto_login_req =   0x1001,
    proto_login_resp =  0x1f01,
    proto_htbt_req =    0x1002,
    proto_htbt_resp =   0x1f02,
    proto_push_req =    0x1003,
    proto_push_resp =   0x1f03
}proto_type_t;

typedef enum proto_version
{
    version1 = 0x0001,
    version2 = 0x0002,
    version3 = 0x0003
    
}proto_version_t;


#endif //__PROTO_CONSTANT_H



