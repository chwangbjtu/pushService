
#ifndef __AGING_TREAT__
#define __AGING_TREAT__

#include "ktimer.h"
#include "tigress_logger.h"
#include "file_info.h"
#include "data_manager.h"

#pragma warning(disable:4996)

class aging_treat:public fsk::ktask
{
	public:
		aging_treat():_dm(NULL){}
		aging_treat(data_manager* p):_dm(p){}
		virtual ~aging_treat(){}

		virtual int run(time_t now)
		{
			map<string,file_info*>::iterator iter;

			_dm->delay_aging(_aging_info);
			for (iter = _aging_info.begin();iter != _aging_info.end();)
			{
				int ret = iter->second->file_delete();
				if (ret > 0)
					KERROR("the file %s delay aging fail", iter->first.c_str())
				else
					KINFO("the file %s has been deleted by delay aging", iter->first.c_str())
				delete iter->second;
				_aging_info.erase(iter++);

				/*
				int ret = 1, ct = 0;
				while(ret > 0 && ct < 5)
				{
					ret = iter->second->file_delete();
					++ct;
					sleep(1);
				}
				if (ret > 0)
				{
					++iter;
					KERROR("the file %s delay aging fail", iter->first.c_str())
				}
				else
				{
					delete iter->second;
					_aging_info.erase(iter++);
					KINFO("the file %s has been deleted by delay aging", iter->first.c_str())
				}*/
			}

			return 0;
		}

	public:
		data_manager* _dm;
		map<string,file_info*> _aging_info;
};

#endif

