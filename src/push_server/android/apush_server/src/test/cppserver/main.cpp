#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <ifaddrs.h>
#include <stdlib.h>
#include <sstream>
#include <arpa/inet.h>
#include <iostream>
#include "http_netio.h"
#include "http_register.h"
#include "http_dispatcher.h"

using namespace std;


int main(int argc,char** argv)
{
    signal(SIGHUP,SIG_IGN);
    signal(SIGPIPE,SIG_IGN);

    sigset_t signal_mask;
    sigemptyset (&signal_mask);
    sigaddset (&signal_mask, SIGPIPE);
    int rc = pthread_sigmask (SIG_BLOCK, &signal_mask, NULL);
    if (rc != 0)
    {
        cout<<"block sigpipe error"<<endl;
        return -1;
    }

    http_register hr;
    hr.start();

     netsvc::epoll_accepter<http_netio> tcp_acceptor;
    //tcp_acceptor.set_max_waittm(5000);
    if(tcp_acceptor.start(8080,8) != 0)
    {
        return -1;
    }        

        while(true)
        {
            sleep(100);
        }
}
