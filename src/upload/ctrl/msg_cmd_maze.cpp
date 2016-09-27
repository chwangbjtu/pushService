#include "msg_cmd_maze.h"

msg_cmd_maze::msg_cmd_maze()
{
	_pfirst= NULL;
	_psecond= NULL;
	_first_send = false;
	_second_send = false;
	_first_send_over = false;
	_second_send_over = false;
	_last_send_first = 0;
	_last_send_second = 0;
	pthread_mutex_init(&_mutex,NULL); 
}

bool msg_cmd_maze::first_send_over()
{
	return _first_send_over;
}

bool msg_cmd_maze::second_send_over()
{
	return _second_send_over;
}

void msg_cmd_maze::set_first_over()
{
	_first_send_over = true;
}

void msg_cmd_maze::set_second_over()
{
	_second_send_over = true;
}

bool msg_cmd_maze::has_first()
{
	if ( _pfirst != NULL)
	{
		return true;
	}

	return false;
}

bool msg_cmd_maze::has_second()
{
	if ( _psecond != NULL)
	{
		return true;
	}

	return false;
}

void msg_cmd_maze::dispatch_first(msg_cmd_base * pmsg)
{
	if ( _pfirst != NULL && pmsg->get_msg_type() == send_transcode)
	{
		delete pmsg;
		pmsg = NULL;
		return ;
	}

	if ( _pfirst != NULL)
	{
		delete pmsg;
		pmsg = NULL;
	}
	else
	{
		_pfirst = pmsg;
	}
	
	if ( pmsg->get_msg_type() == send_transcode)
	{
		_first_send = true;
		_first_send_over = true;
		_psecond = pmsg;
	}
}

void msg_cmd_maze::dispatch_second(msg_cmd_base * pmsg)
{
	if ( _psecond != NULL)
	{
		string msg = pmsg->get_msg();
		_psecond->set_msg(msg);
		delete pmsg;
		pmsg = NULL;
	}
	else
	{
		_psecond = pmsg;
	}
}

msg_cmd_base * msg_cmd_maze::get_msg()
{
	pthread_mutex_lock(&_mutex);

	msg_cmd_base * pcmd = NULL;
	//if ( !_first_send_over && !_first_send && _pfirst != NULL)//如果begin未发送，先发送begin
	time_t now = time(NULL);
	if ( !_first_send_over && _pfirst != NULL && now - _last_send_first > 2)//如果begin未发送，先发送begin
	{
		_first_send = true;
		pcmd = _pfirst;
		_last_send_first = now;
	}

	//if ( pcmd == NULL &&  _first_send_over && !_second_send_over && !_second_send && _psecond != NULL)//
	if ( pcmd == NULL &&  _first_send_over && !_second_send_over && _psecond != NULL && now - _last_send_second > 2)//
	{
		_second_send = true;
		pcmd = _psecond;
		_last_send_second = now;
	}

	pthread_mutex_unlock(&_mutex);
	return pcmd;
}

void msg_cmd_maze::send_error(msg_cmd_base * pmsg)
{
	if (pmsg->get_msg_type() == send_transcode)
	{
		_second_send = false;
	}
	else if (pmsg->get_msg_type() == send_upload_begin)
	{
		_first_send = false;
	}
	else if (pmsg->get_msg_type() == send_upload_finish)
	{
		_second_send = false;
	}
}

void msg_cmd_maze::delete_all_cmd()
{
	if ( _pfirst == _psecond)
	{
		delete _pfirst;
		_pfirst = NULL;
	}
	else
	{
		delete _pfirst;
		_pfirst = NULL;
		delete _psecond;
		_psecond = NULL;
	}
}


