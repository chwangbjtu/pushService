#include <iostream>
#include <signal.h>

#include "tcp_service.h"

#include "dbg.h"
#include "configure.h"

#include "user_mgr.h"
#include "msg_mgr.h"

#include "tcp_netio.h"
#include "proto_register.h"

#include "http_netio.h"
#include "http_register.h"

#include "util.h"
#include "msg_manager.h"
#include "visitor.h"
#include "tlogger.h"
#include "task_timer.h"


using namespace std;



int main(int argc,char* argv[])
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


    if ( argc == 2 && strncmp(argv[1], "-v", 2) == 0 )
    {
        printf("aputhserver %s build at %s\r\n", APUSH_SERVER_VERSION, MAKEFILEBUILD_DATE);
        return 0;
    }

    if ( configure::instance()->start("./etc/ct_config.ini") < 0)
    {   
        return -1;
    }

    string apptype = configure::instance()->get_app_type();
    int res = util::instance()->set_app_type(apptype);
    if ( res != 0)
    {
        DBG_ERROR("config app type error");
        return -1;
    }

    user_mgr::instance();
	user_mgr::instance()->start(configure::instance()->get_service_worker_num(),configure::instance()->get_max_user_num());
	msg_mgr::instance();
    DBG_INFO("start user_msg ok");

    msg_manager::instance();
    util::instance();
    visitor::instance()->start();

    proto_register protoregister;
    protoregister.start();

	http_register httpregister;
	httpregister.start();

    //logger
    if(tlogger::instance()->start() < 0)
    {   
        DBG_ERROR("start logger error");
        return -1;
    }
    
    task_timer::instance()->start();

	//start mgmt
	netsvc::epoll_accepter<http_netio> mgmt_acceptor;
	if(mgmt_acceptor.start(configure::instance()->get_mgmt_port(),
        configure::instance()->get_mgmt_worker_num()) != 0)
    {
        DBG_ERROR("start mgmt accepter failed.");
        return -1;
    }

    //start tcp
    netsvc::epoll_accepter<tcp_netio> tcp_acceptor;
    tcp_acceptor.set_dispatch(least);
    //tcp_acceptor.set_max_waittm(5000);
    if(tcp_acceptor.start(configure::instance()->get_service_port(),
        configure::instance()->get_service_worker_num()) != 0)
    {
        DBG_ERROR("start tcp accepter failed.");
        return -1;
    }

    while(true)
    {
        sleep(100000);
    }

    return 0;

}
