#include <sys/types.h>
#include <ifaddrs.h>
#include <stdlib.h>
#include <sstream>
#include <arpa/inet.h>
#include "dbg.h"
#include "soc_mgr.h"

soc_mgr::soc_mgr()
{
    _id = 0;
    _id1 = 0;
    _gb = "{\"token\":\"";//782BCBA20961
    _ge =  "\",\"mac\":\"782BCBA20961\",\"version\":\"1.2.3.4\",\"last_msg_id\":\"0\",\"last_push_id\":\"0\",\"app_name\":\"apad\"}";

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

int soc_mgr::start(int htbt_interval)
{
    for(int i=0;i<51000;i++)
    {
        //list<string> tlist;
        //_recvmsgid.push_back(tlist);
        _recvmsgid.push_back(-1);
        _loginflag.push_back(0);
    }

    _htbt_interval = htbt_interval;
}

int soc_mgr::get_htbt_interval()
{
    return _htbt_interval;
}

int soc_mgr::get_id()
{
    int id = 0;
    pthread_mutex_lock(&_hmutex);
    id = _id;
    _id++;
    pthread_mutex_unlock(&_hmutex);
    return id;
}

int soc_mgr::get_id1()
{
    int id = 0;
    pthread_mutex_lock(&_hmutex);
    id = _id1;
    _id1++;
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
        ph->_type = htons(0x1001);
        stringstream ss;
        ss<<_gb<<_shost<<"."<<id<<_ge;
        ph->_length = htonl(ss.str().size()+16);
        //ph->_length = ss.str().size()+16;
        str.append(ss.str());
    }
    else if ( type == "htbt")
    {
        ph->_reserved = 0x32000000;
        ph->_type = htons(0x1002);
        ph->_length = htonl(16);
        
    }
    else if ( type == "push")
    {
        string ttstr;
        //int size = _recvmsgid[id].size();
        //list<string>::iterator iter = _recvmsgid[id].begin();
        //for( ;iter !=  _recvmsgid[id].end();iter++)
        {
            string str1;
            str1.assign(sizeof(header),'\0');
            header * ph = (header *)str1.data();
            ph->_version = htons(1);
            ph->_type = htons(0x1003);
            string tmsg = "{\"msgid\":\"";
            stringstream ss;
            ss<<_recvmsgid[id];
            tmsg.append(ss.str());
            tmsg.append("\"}");
            ph->_length = htonl(tmsg.size()+16);
            //ph->_msgid = htonl(atoi((*iter).data()));
            //ph->_msgid = htonl(_recvmsgid[id]);
            ttstr.append(str1);
            ttstr.append(tmsg);
        }
        //_recvmsgid[id].clear();
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
        _loginflag[id] = 1;
    }
    else
    {
        if ( _recvmsgid[id] > 0)
        {
            msg = get_msg("push",id);
            _recvmsgid[id] = -1;
        }
        else
        {
            msg = get_msg("htbt",id);
        }
    }

    return msg;
}

string soc_mgr::get_push_msg(int id)
{
    string msg;
    {
        if ( _recvmsgid[id] > 0)
        {
            msg = get_msg("push",id);
            _recvmsgid[id] = -1;
        }
    }

    return msg;
}

int soc_mgr::push_msgid(int fd,string msgid)
{
    //_recvmsgid[fd].push_back(msgid);
    // 
    pthread_mutex_lock(&_hmutex);
    //_msgid = msgid;
    int imsgid = atoi(msgid.data());
    if ( _recvmsgid[fd] < 0)
        _recvmsgid[fd] = imsgid;
    pthread_mutex_unlock(&_hmutex);
    return 0;
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
