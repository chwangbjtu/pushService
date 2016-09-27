#include "http_def.h"
#include "http_util.h"

BEGIN_FS_NAMESPACE

request_t::request_t():
_method("GET"),
_path_and_parameters(""),
_path("/"),
_version("1.1"),
_paramstr("")
{
}

request_t::~request_t()
{
    this->reset();
}

void request_t::reset()
{
    _method = "";
	_path_and_parameters = "";
	_path = "";
	_paramstr = "";
	_version = "";
    _content = "";;

	_map_params.clear();
	_map_headers.clear();
}

int request_t::get_message_header(char* key,string& value)
{
    return get_message(type_header,key,value);
}

int request_t::get_param(char* key,string& value)
{
    return get_message(type_parameter,key,value);
}

int request_t::get_message(int type,char* key,string& value)
{
    multimap<string,string>* m = NULL;
    switch( type )
    {
    case type_header:
        m = &_map_headers;
        break;
    case type_parameter:
        m = &_map_params;
        break;
    default:
        return -1;
    }

    int ret = -1;
    string key_lowcase;
    LOWCASE(key,key + strlen(key) - 1 ,key_lowcase);
    multimap<string,string>::iterator it = m->find(key_lowcase);
    if( it != m->end() )
    {
        value = it->second;
        ret = 0;
    }
    return ret;
}

int request_t::set_message(int type,char* key,string& value)
{
    multimap<string,string>* m = NULL;
    switch( type )
    {
    case type_header:
        m = &_map_headers;
        break;
    case type_parameter:
        m = &_map_params;
        break;
    default:
        return -1;
    }

    m->insert(make_pair<string,string>(string(key),value));
    return 0;
}

int request_t::add_message_header(char* key,string& value)
{
    return set_message(type_header,key,value);
}

string request_t::get_content_length()
{
    string length_str;
    int ret = get_message_header("content-length",length_str);
    if( ret < 0 )
    {
        return "";
    }

    return length_str;
}




response_t::response_t():
    _version("1.1"),
    _code("200"),
    _code_info("OK"),
    _content("")
{
}

response_t::~response_t()
{
    this->reset();
}

int response_t::get_message_header(char* key,string& value)
{
    int ret = -1;
    string key_lowcase;
    LOWCASE(key,key + strlen(key) - 1 ,key_lowcase);
    multimap<string,string>::iterator it = _map_headers.find(key_lowcase);
    if( it != _map_headers.end() )
    {
        value = it->second;
        ret = 0;
    }

    return ret;
}

int response_t::add_message_header(char* key,string& value)
{
    _map_headers.insert(make_pair<string,string>(string(key),value));
    return 0;
}

void response_t::reset()
{
    _version = "";
	_code = "";
	_code_info = "";
	_map_headers.clear();
	_content = "";
}



END_FS_NAMESPACE
