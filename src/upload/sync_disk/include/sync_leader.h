
#ifndef __SYNC_LEADER__
#define __SYNC_LEADER__

#include <pthread.h>
#include "cmdq.h"

//class cmdq;

//const int SYNC_DISK_THREAD_COUNT = 2;

class sync_leader
{
public:	
	sync_leader();
	~sync_leader();

	int start(std::string& res);
	//int sync_send(void* arg);
	int flush_to_disk(void* arg, char* pstart, int len);
	int flush_meta_to_disk(void* arg);
	static void* thread_func(void *arg);
private:
	pthread_t* _tid; //[SYNC_DISK_THREAD_COUNT];
	fsk::cmdq* _cmd; //[SYNC_DISK_THREAD_COUNT];
	int SYNC_DISK_THREAD_COUNT;
	struct cmd_t
	{
		int _current_cmdq;
		void* psl;
	};
};

#endif

