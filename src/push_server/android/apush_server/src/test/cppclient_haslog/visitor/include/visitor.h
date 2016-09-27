#ifndef __VISITOR_H
#define __VISITOR_H

#include <vector>
#include "visitor_handler.h"
#include "tconnector.h"

using namespace std;

class visitor
{
public:
    ~visitor();

    static visitor* instance();
    int start();

    int connect(unsigned int ip,unsigned short port);
private:
    visitor();
    static visitor* _instance;

    tconnector<visitor_handler> * _pconnector;
    
    pthread_t _thread_connector;
    
    static void * connect_thread(void *arg);
};

#endif//__VISITOR_H


