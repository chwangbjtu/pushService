#ifndef __SOC_MGR_H
#define __SOC_MGR_H

#include <pthread.h>
#include <iostream>
#include <vector>
#include <list>

using namespace std;

#pragma pack(1)
class header
{
public:
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
    /*
    unsigned short _version;
    unsigned short _type;
    unsigned int _length;
    */
};

class rresp
{
public:
    unsigned short _version;
    unsigned short _type;
    unsigned int _length;
    unsigned int _msgid;
};

#pragma pack()

class soc_mgr
{
public:
    string get_msg(string type,int id);
    string get_msg(int id);
    string get_push_msg(int id);
    string get_htbt();
    int start(int htbt_interval);
    int get_htbt_interval();
    int get_id();
    int get_id1();
    int push_msgid(int fd,string msgid);
    string get_host();
     static soc_mgr * instance();
public:
     soc_mgr();
    static soc_mgr * _inst;
public:
    string _gb;
    string _ge;
    vector<string> _htbtmsg;
    vector<string> _pushmsg;
    //vector<list<string> > _recvmsgid;
    vector<int> _recvmsgid;
    vector<int> _loginflag;
    vector<int> _fds;
    int _id;
    int _id1;
    string _msgid;
    string _shost;

    int _htbt_interval;

    pthread_mutex_t _hmutex;
};

#endif//__SOCK_MGR_H
