
#include <signal.h>
#include "tigress_logger.h"
#include "tcp_service.h"
#include "data_manager.h"
#include "video_get_leader.h"
#include "video_accept_handler.h"
//#include "video_post_leader.h"
#include "tigress_leader.h"
#include "tigress_conf.h"
#include "info_leader.h"
#include "sync_leader.h"

#include "msg_manager.h"
#include "visitor.h"

using namespace std;

int show_version(int argc,char* argv[])
{
	int ret = -1;
	int result = 0;

	while ((ret = getopt(argc,argv,"v") ) != -1)
	{
		result = 1;
		switch (ret)
		{
			case 'v':
				printf("version : %s, build at %s\n",TIGRESS_VERSION,MAKEFILEBUILD_DATE);//////////////////////
				break;
			default:
				break;
		}
	}

	return result;
}

int main(int argc, char* argv[])
{
	if (SIG_ERR == signal(SIGHUP,SIG_IGN) || SIG_ERR == signal(SIGPIPE,SIG_IGN))
	{
		cout<<"can not ignore the signal SIGHUP or SIGPIPE"<<endl;
		return 0;
	}

	if (show_version(argc,argv))
	{
		return 0;
	}

	if (NULL == tigress_logger::get_instance())
	{
		cout<<"tigress_logger start fail!"<<endl;
		return 0;
	}

	if (NULL == tigress_conf::get_instance() || 0 != tigress_conf::get_instance()->open("./etc/tigress.ini", "./etc/tigress_default.ini"))
	{
		cout<<"tigress configure start fail!"<<endl;
		return 0;
	}

	msg_manager::instance()->start();
	visitor::instance()->start();

	string res;

	if (0 != tigress_leader::get_instance()->start(res))
	{
		cout<<res<<endl;
		return 0;
	}

	while (true)
	{
		sleep((unsigned int)-1);
	}

	return 0;
}


