

#ifndef __TIGRESS_LOGGER__
#define __TIGRESS_LOGGER__

#include <string>
#include "logger.h"

class tigress_logger
{
	public:
		~tigress_logger();

		static void set_filter_level(std::string& s);

		static fsk::logger* get_instance();

	private:
		tigress_logger();

		static fsk::logger* _instance;
};

#define KLOG(msg, dbg_level) do{\
			fsk::location_t loc(__FILE__, __LINE__);\
			fsk::logitem_t item(msg, dbg_level, loc);\
			tigress_logger::get_instance()->log(&item);\
		}while(0)

#define KTRACE(format,args...) do {char __msg[MAX_LOGMSG_SIZE] = {0};snprintf(__msg, MAX_LOGMSG_SIZE-1, format, ##args);KLOG(__msg, fsk::level_t::trace_level());}while (0);
#define KDEBUG(format,args...) do {char __msg[MAX_LOGMSG_SIZE] = {0};snprintf(__msg, MAX_LOGMSG_SIZE-1, format, ##args);KLOG(__msg, fsk::level_t::debug_level());}while (0);
#define KINFO(format,args...) do {char __msg[MAX_LOGMSG_SIZE] = {0};snprintf(__msg, MAX_LOGMSG_SIZE-1, format, ##args);KLOG(__msg, fsk::level_t::info_level());tigress_logger::get_instance()->flush();}while (0);
#define KWARN(format,args...) do {char __msg[MAX_LOGMSG_SIZE] = {0};snprintf(__msg, MAX_LOGMSG_SIZE-1, format, ##args);KLOG(__msg, fsk::level_t::warn_level());tigress_logger::get_instance()->flush();}while (0);
#define KERROR(format,args...) do {char __msg[MAX_LOGMSG_SIZE] = {0};snprintf(__msg, MAX_LOGMSG_SIZE-1, format, ##args);KLOG(__msg, fsk::level_t::error_level());tigress_logger::get_instance()->flush();}while (0);
#define KFATAL(format,args...) do {char __msg[MAX_LOGMSG_SIZE] = {0};snprintf(__msg, MAX_LOGMSG_SIZE-1, format, ##args);KLOG(__msg, fsk::level_t::fatal_level());tigress_logger::get_instance()->flush();}while (0);

#endif

