// =====================================================================================
// 
//       Filename:  json.cpp $Id$:
// 
//    Description:  
// 
//        Created:  10/09/2012 02:07:36 PM CST
//       Revision:  $Rev$:
//       Compiler:  g++
// 
//         Author:  liubo (lb), lb.falcons@gmail.com ($Author$:)
//        Company:  funshion
// 
// =====================================================================================

#include <sstream>
#include "json.h"
#include "json/writer.h"

using namespace pandaria;
json::json()
{

}

json::~json()
{

}

json::json(Json::Value& v)
    :_value(v)
{

}

int json::add(string& key,string& value)
{
    _value[key] = value;
    return 0;
}

int json::add(string& key,int value)
{
    _value[key] = value;
    return 0;
}

int json::add(string& key,long long  value)
{
    std::stringstream s;
    s << value;
    _value[key] = s.str();
    return 0;
}

int json::add(string& key,json& value)
{
    _value[key] = value.get_value();
    return 0;
}

int json::add(char* key,string& value)
{
    _value[string(key)] = value;
    return 0;
}

int json::add(char* key,int value)
{
    _value[string(key)] = value;
    return 0;
}

int json::add(char* key,long long value)
{
    std::stringstream s;
    s << value;
    _value[key] = s.str();
    return 0;
}

int json::add(char* key,char* value)
{
    _value[string(key)] = string(value);
    return 0;
}

int json::add(char* key,json& value)
{
    _value[string(key)] = value.get_value();
    return 0;
}

int json::append(string& key,string& value)
{
    _value[key].append(value);
    return 0;
}

int json::append(string& key,int value)
{
    _value[key].append(value);
    return 0;
}

int json::append(string& key,long long value)
{
    std::stringstream s;
    s << value;
    _value[key] = s.str();
    return 0;
}

int json::append(string& key,json& value)
{
    _value[key].append(value.get_value());
    return 0;
}

int json::append(char* key,string& value)
{
    _value[string(key)].append(value);
    return 0;
}

int json::append(char* key,char* value)
{
    _value[string(key)].append(value);
    return 0;
}

int json::append(char* key,int value)
{
    _value[string(key)].append(value);
    return 0;
}

int json::append(char* key,long long value)
{
    std::stringstream s;
    s << value;
    _value[string(key)] = s.str();
    return 0;
}

int json::append(char* key,json& value)
{
    _value[string(key)].append(value.get_value());
    return 0;
}

Json::Value& json::get_value()
{
    return _value;
}

string json::to_formated_str()
{
    Json::FastWriter fw;
    return fw.write(_value);
    //return _value.toStyledString();
}

bool json::parse(string& s,string& error_info)
{
    if( ! _value.empty() )
    {
        _value.clear();
    }

    Json::Reader r;
    bool ret = r.parse(s,_value);
    if( ret == false )
    {
        error_info = r.getFormatedErrorMessages();
    }
    return ret;
}

int json::get(string& key,int default_value,string& errinfo)
{
    int ret ;
    try
    {
        ret = _value.get(string(key),default_value).asInt();
    }
    catch( const exception& ex)
    {
        errinfo = ex.what();
        ret = -1;
    }
    return ret;
}

int json::get(char* key,int default_value,string& errinfo)
{
    int ret ;
    try
    {
        ret = _value.get(string(key),default_value).asInt();
    }
    catch( const exception& ex)
    {
        errinfo = ex.what();
        ret = -1;
    }
    return ret;
}

string json::get(string& key,string& default_value,string& err)
{
    string ret ;
    try
    {
        ret = _value.get(key,default_value).asString();
    }
    catch( const exception& ex)
    {
        err = ex.what();
        ret = "";
    }
    return ret;

}

string json::get(char* key,string& default_value,string& errinfo)
{
    string ret ;
    try
    {
        ret = _value.get(string(key),default_value).asString();
    }
    catch( const exception& ex)
    {
        errinfo = ex.what();
        ret = "";
    }
    return ret;
}

int json::get(string& key,json& j,string& err)
{
    int ret = -1;
    bool member = _value.isMember(key);
    if( member == true )
    {
        j.get_value() = (_value[key]);
        ret = 0;
    }
    else
    {
        ret = -1;
        err = "no the member";
    }
    return ret;
}

int json::get(char* key,json& j,string& errinfo)
{
    int ret = -1;
    bool member = _value.isMember(string(key));
    if( member == true )
    {
        j.get_value() = (_value[key]);
        ret = 0;
    }
    else
    {
        ret = -1;
        errinfo = "no the member";
    }
    return ret;
}

int json::get_array(vector<json>& v)
{
    if( !_value.isArray() )
    {
        return -1;
    }

    v.reserve(_value.size());

    Json::Value::iterator it = _value.begin(),it_end = _value.end();
    while( it != it_end )
    {
        v.push_back(json(*it++));
    }
    return 0;
}

string json::get_string()
{
    return _value.asString();
}

int json::get_int()
{
    return _value.asInt();
}
