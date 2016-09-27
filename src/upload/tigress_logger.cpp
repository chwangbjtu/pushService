
#include <iostream>
#include "tigress_logger.h"
#include "time_point_logger.h"
#include "writer_file.h"
#include "layout_pattern.h"
#include "filter_level.h"

using namespace std;

fsk::logger* tigress_logger::_instance = NULL;

tigress_logger::tigress_logger()
{

}

tigress_logger::~tigress_logger()
{
	if (NULL != _instance)
	{
		_instance->close();
		delete _instance;
		_instance = NULL;
	}
}

fsk::logger* tigress_logger::get_instance()
{
	if (NULL == _instance)
	{
		_instance = new fsk::time_point_logger("tigress_%Y%m%d.log", fsk::daytime(23,59), new fsk::writer_file("./log"));//need configure file 
		_instance->set_layout(new fsk::layout_pattern("[%t][%T][%l] %m [%L]\r\n"));
		//string lev("info");
		string lev("debug");
		set_filter_level(lev);////////////////
		int ret = _instance->open();
		if (ret != 0)
		{
			return NULL;
			//cout<<"open logger file failed"<<endl;
		}
		else
		{
			KTRACE("%s","open logger file success");
		}
	}

	return _instance;
}

void tigress_logger::set_filter_level(string& s)
{
	if ("trace" == s)
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::trace_level()));
	}
	else if ("debug" == s)
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::debug_level()));
	}
	else if ("info" == s)
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::info_level()));
	}
	else if ("warn" == s)
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::warn_level()));
	}
	else if ("error" == s)
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::error_level()));
	}
	else if ("fatal" == s)
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::fatal_level()));
	}
	else if ("off" == s)
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::off_level()));
	}
	else
	{
		_instance->set_filter(new fsk::filter_level(fsk::level_t::info_level()));
	}
}

