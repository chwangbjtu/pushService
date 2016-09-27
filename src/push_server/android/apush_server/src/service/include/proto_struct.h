#ifndef __PROTO_STRUCT_H
#define __PROTO_STRUCT_H
#pragma pack(1)
//#define  PROTO_HEADER_LEN   16

typedef struct header_struct
{
    unsigned int _reserved;
    //length of the datagram
    unsigned int _length;
    //protocol type of the datagram
    unsigned short _type;
    //version of the protocol type
    unsigned short _version;
    //session id of the datagram
    unsigned short _session_id;
    //reserved for check sum
    unsigned short _checksum;
    inline int size()
    {
        return sizeof(struct header_struct);
    }
} header_struct_t;


#pragma pack()


#endif//__PROTO_STRUCT_H

