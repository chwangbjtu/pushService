// =====================================================================================
// 
//       Filename:  json.h $Id$:
// 
//    Description:  
// 
//        Created:  10/10/2012 09:28:26 AM CST
//       Revision:  $Rev$:
//       Compiler:  g++
// 
//         Author:  liubo (lb), lb.falcons@gmail.com ($Author$:)
//        Company:  funshion
// 
// =====================================================================================

#ifndef JSON_H
#define JSON_H 

#include <string>
#include "json/json.h"

using namespace std;

namespace pandaria
{
    class json
    {
    public:
        json();
        ~json();
        json(Json::Value& v);

    public:
        /*
         * add a pair(key,value) in a json node.
         *  key's type must be string
         *  value's type can be string,int,a json node
         * @param key : key name,string type
         * @param value : key's value
         *
         * return 
         *  0 - ok , other fail
         *  */
        int add(string& key,string& value);
        int add(string& key,int value);
        int add(string& key,long long value);
        int add(string& key,json& value);

        /*
         * add a pair(key,value) in a json node
         *  key's type must be a char*
         *  value's type can be string,int,a json node,char*
         * @param key : key name,string type
         * @param value : key's value
         *
         * return 
         *  0 - ok , other fail
         *  */
        int add(char* key,string& value);
        int add(char* key,int value);
        int add(char* key,long long value);
        int add(char* key,char* value);
        int add(char* key,json& value);

        /*
         * add a value in array,ONLY USE WITH A ARRAY
         *  key's type must be string or char*
         *  value's type can be string,int,json node
         * @param key : key's name
         * @param value : key's value
         *
         * return
         *  0 - ok, other fail
         *  */
        int append(string& key,string& value);
        int append(string& key,int value);
        int append(string& key,long long value);
        int append(string& key,json& value);
        int append(char* key,string& value);
        int append(char* key,char* value);
        int append(char* key,int value);
        int append(char* key,long long value);
        int append(char* key,json& value);


        /*
         * output the json string.
         *
         * return
         *  the json string
         *  */
        string to_formated_str();

        /*
         * parse the json string.
         *
         * @param  s : json string
         * @param error_info : if error,the error info save in it
         *
         * return 
         *  true : parse ok, false : parse fail
         *  */
        bool parse(string& s,string& error_info);

        /*
         * get node's value, the node can be a string,int,array.
         * Because of the array can have a array,int or string,so just return a node
         *  @param key : key name
         *  @param default_value : the key's default value
         *  @param errinfo : if get fail,error info in it
         *
         * return
         *  int     ok,the value    fail: -1
         *  string  ok,the value    fail: ""
         * */
        int get(string& key,int default_value,string& errinfo);
        int get(char* key,int default_value,string& errinfo);
        string get(string& key,string& default_value,string& err);
        string get(char* key,string& default_value,string& errinfo);
        int get(string& key,json& j,string& err);
        int get(char* key,json& j,string& errinfo);

        /*
         * for array operate. MAKE SURE the node is array.
         * */
        int get_array(vector<json>& v);

        /*
         * get the element's vaule in the array
         * */
        string get_string();
        int get_int();

        /*
         * return a Json::Value object. user don't need it.
         * But for support Recursion,the lib need it
         **/
        Json::Value& get_value();
    private:
        Json::Value _value;
    };
}
#endif /* JSON_H */
