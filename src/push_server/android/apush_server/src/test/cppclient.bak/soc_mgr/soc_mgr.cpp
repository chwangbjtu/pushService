#include <sys/types.h>
#include <ifaddrs.h>
#include <stdlib.h>
#include <sstream>
#include <arpa/inet.h>
#include "soc_mgr.h"

soc_mgr::soc_mgr()
{
    _id = 0;
    _gb = "{\"fudid\":\"";//782BCBA20961
    _ge =  "\",\"mac\":\"782BCBA20961\",\"version\":\"1.2.3.4\",\"last_msg_id\":\"0\"}";

    pthread_mutex_init(&_hmutex, NULL);

    _shost = get_host();
}

soc_mgr* soc_mgr::_inst = NULL;

soc_mgr* soc_mgr::instance()
{
    if ( _inst == NULL)
        _inst = new soc_mgr();
    return _inst;
}

int soc_mgr::start()
{
    for(int i=0;i<50000;i++)
    {
        list<string> tlist;
        _recvmsgid.push_back(tlist);
        _loginflag.push_back(0);
    }
}

int soc_mgr::get_id()
{
    pthread_mutex_lock(&_hmutex);
    int id = _id++;
    pthread_mutex_unlock(&_hmutex);
    return id;
}

string soc_mgr::get_msg(string type,int id)
{
    string str;
    str.assign(sizeof(header),'\0');
    header * ph = (header *)str.data();
    ph->_version = htons(1);

    if ( type == "login")
    {
        ph->_type = htons(1);
        stringstream ss;
        ss<<_gb<<_shost<<"."<<id<<_ge;
        ph->_length = htonl(ss.str().size());
        str.append(ss.str());
    }
    else if ( type == "push")
    {
        string ttstr;
        int size = _recvmsgid[id].size();
        list<string>::iterator iter = _recvmsgid[id].begin();
        for( ;iter !=  _recvmsgid[id].end();iter++)
        {
            string str1;
            str1.assign(sizeof(rresp),'\0');
            rresp * ph = (rresp *)str1.data();
            ph->_version = htons(1);
            ph->_type = htons(3);
            ph->_length = htonl(4);
            ph->_msgid = htonl(atoi((*iter).data()));
            ttstr.append(str1);
        }
        _recvmsgid[id].clear();
        str = ttstr;
    }

    return str;
}

string soc_mgr::get_msg(int id)
{
    string msg;
    if ( _loginflag[id] == 0)
    {
        msg = get_msg("login",id);
    }
    else
    {
        msg = get_msg("htbt",id);
    }

    return msg;
}

int soc_mgr::push_msgid(int fd,string msgid)
{
    _recvmsgid[fd].push_back(msgid);
}

string soc_mgr::get_host()
{
    struct ifaddrs * ifAddrStruct=NULL;
    void * tmpAddrPtr=NULL;

    getifaddrs(&ifAddrStruct);

    while (ifAddrStruct!=NULL) {
        if (ifAddrStruct->ifa_addr->sa_family==AF_INET) { // check it is IP4
            tmpAddrPtr=&((struct sockaddr_in *)ifAddrStruct->ifa_addr)->sin_addr;
            char addressBuffer[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, tmpAddrPtr, addressBuffer, INET_ADDRSTRLEN);
            string str(ifAddrStruct->ifa_name);
            if ( str.find("lo") == string::npos)
            {
                string tname(addressBuffer);
                return tname;
            }
        }
        ifAddrStruct=ifAddrStruct->ifa_next;
    }
    string ttname;
    return ttname;
}
