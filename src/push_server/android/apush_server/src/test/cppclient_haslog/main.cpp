#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <ifaddrs.h>
#include <stdlib.h>
#include <sstream>
#include <arpa/inet.h>
#include <iostream>
#include "dbg.h"
#include "proto_register.h"
#include "proto_dispatcher.h"
#include "soc_mgr.h"
#include "visitor.h"

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

        if ( argc != 5)
        {
                cout<<"a.out ip port clientnum htbtinterval"<<endl;
                return -1;
        }


        unsigned int ip;
        unsigned short port;

        in_addr ipaddr1;
        memset(&ipaddr1,0,sizeof(ipaddr1));
        if(inet_pton(AF_INET,argv[1],(struct in_addr*)&ipaddr1)>0)
        {
                ip = htonl(ipaddr1.s_addr);
        }

        port = atoi(argv[2]);
        int client_num = atoi(argv[3]);
        int htbt_interval = atoi(argv[4]);

        proto_register aaa;
        aaa.start();
        proto_dispatcher::instance();

        soc_mgr::instance()->start(htbt_interval);

        visitor::instance()->start();
        int j = 0;

        for(int i=0;i<client_num;i++)
        {
            j++;
            if ( j % 1000 == 0)
            {
                sleep(0.5);
            }
            visitor::instance()->connect(ip,port);
            //DBG_INFO("%d",i);
        }


        while(true)
        {
            sleep(100);
        }
}
