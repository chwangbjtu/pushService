
#include <iostream>
#include "tigress_conf.h"
#include "sync_leader.h"
#include "sync_disk.h"

sync_leader::sync_leader():_tid(NULL), _cmd(NULL), SYNC_DISK_THREAD_COUNT(2)
{
	tigress_conf::get_instance()->get_integer_value("sync_disk", "thread_num", SYNC_DISK_THREAD_COUNT);
	_tid = new pthread_t[SYNC_DISK_THREAD_COUNT];
	_cmd = new fsk::cmdq[SYNC_DISK_THREAD_COUNT];
}

sync_leader::~sync_leader()
{
	delete[] _tid;
	delete[] _cmd;
}

int sync_leader::start(std::string& res)
{
	for(int i = 0;i < SYNC_DISK_THREAD_COUNT;i++)
	{
		struct cmd_t* st = new struct cmd_t;
		st->_current_cmdq = i;
		st->psl = (void*)this;
		pthread_create(&_tid[i], 0, &thread_func, (void*)st);
	}
	return 0;
}
/*
int sync_leader::sync_send(void* arg)
{
	_cmd.post(arg);
	return 0;
}
*/

int sync_leader::flush_meta_to_disk(void* arg)
{
	sync_disk* sd = new sync_disk;
	sd->init(arg, NULL, 0);
	sd->flush_meta_to_disk();
	delete sd;

/*	
	sync_disk* sd = new sync_disk;
	sd->init(arg, pstart, len);
	_cmd[((long)arg % SYNC_DISK_THREAD_COUNT)].post((void*)sd);
	return 0;
*/
}

int sync_leader::flush_to_disk(void* arg, char* pstart, int len)
{
	sync_disk* sd = new sync_disk;
	sd->init(arg, pstart, len);
	sd->flush_to_disk();
	delete sd;

/*	
	sync_disk* sd = new sync_disk;
	sd->init(arg, pstart, len);
	_cmd[((long)arg % SYNC_DISK_THREAD_COUNT)].post((void*)sd);
	return 0;
*/
}

void* sync_leader::thread_func(void* arg)
{
	struct cmd_t* st = (struct cmd_t*)arg;
	sync_leader* sl = (static_cast<sync_leader*>(st->psl));//(sync_leader*)arg;
	int current_q = st->_current_cmdq;
	int ret = -1;
	void* sd = NULL;
	while (true)
	{
		ret = sl->_cmd[current_q].peek(sd, -1);//wait until a command has peeked
		//ret = sl->_cmd[current_q].recv(sd);//wait until a command has peeked
		if (0 == ret)
		{
			(static_cast<sync_disk*>(sd))->flush_to_disk();
			delete (static_cast<sync_disk*>(sd));
		}
	}

	delete st;
	pthread_exit(0);
	return NULL;
}
