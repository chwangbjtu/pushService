#ifndef __HTTP_CONSTANT_H
#define __HTTP_CONSTANT_H
#include <string>
#include <map>
#include <iostream>
#include "k_ns.h"

BEGIN_FS_NAMESPACE

using namespace std;

/*data type to save http request parse results*/
struct request_t
{
	request_t();
	~request_t();

	//http request method
	string _method;
	//http request path and parameter
	string _path_and_parameters;
	//request path
	string _path;
	//http version
	string _version;
	//parameters string
	string _paramstr;
    // message body,if has
    string _content;

	//request parameters
	multimap<string, string> _map_params;
	//request headers
	multimap<string, string> _map_headers;

	//request cookies, !!current not used!! 
    //when in using , open it. @lb
	//multimap<string, string> _map_cookies;

    void reset();
    /*
     * get a message header's value , e.g  key like "Host"
     *
     * return 
     *  0 ok,the value is in the v
     *  -1 fail
     **/
    int get_message_header(char* key,string& value);
    int get_param(char* key,string& value);

    /*
     * add a message header 
     * @parameter key : field name
     * @parameter value : field value
     *
     * return 
     *  0 - ok , -1 fail
     *  */
    int add_message_header(char* key,string& value);


    // =================== wrapper of get message header's value  =================================
    /*
     * get url,only include the url,dont's include parameter in url
     *
     * return 
     *  url
     *  */
    string get_url(){ return _path;};

    /*
     * get Host's value
     * return 
     *  0 ok , -1 fail 
     *  0 ok ,range's value is in host_name, -1 fail 
     * */
    int get_host(string& host_name){ return get_message_header("host",host_name);}

    /*
     * get Content-Length's value
     *
     * return 
     *  ok, the length or -1 if fail
     *  */
    string get_content_length();

    /*
     * get Range's value
     *
     * return
     *  0 ok ,range's value is in v, -1 fail 
     *  */
    int get_range(string& v){return get_message_header("range",v);}
private:
    enum map_type{
        type_unknown = 0,
        type_parameter,
        type_header
    };
    int get_message(int type,char* key,string& value);
    int set_message(int type,char* key,string& value);
};

/*data type to save http response results*/
struct response_t 
{
	response_t();
	~response_t();

	//http version
	string _version;
	//response code
	string _code;
	//response code info
	string _code_info;
	//response header parameters
	multimap<string, string> _map_headers;
	//response content
	string _content;

    /*
     * get a message header's value , e.g  key like "Host"
     *
     * return 
     *  0 ok,the value is in the v
     *  -1 fail
     **/
    int get_message_header(char* key,string& value);

    /*
     * add a message header 
     * @parameter key : field name
     * @parameter value : field value
     *
     * return 
     *  0 - ok , -1 fail
     *  */
    int add_message_header(char* key,string& value);


    // ================================ wrap for get/add_message_header() =============
    int set_connection(string& value ){return add_message_header("Connection",value);}

    int set_connection(char* value ){string v(value); return add_message_header("Connection",v);}

    int get_connection(string& value){ return get_message_header("connection",value);}

    void reset();
};

//response encode types
typedef enum encode_type
{
	NONE = 0,
	GZIP = 1,
	DEFLATE = 2
}encode_type;

#define SEP_LINE				"\r\n"
#define HEADER_END				"\r\n\r\n"
#define SEP_GET					' '
#define SEP_URL					' '
#define SEP_SPACE				' '
#define SEP_QM					'?'
#define SEP_EQ					'='
#define SEP_AND					'&'
#define SEP_VERSION				'/'
#define SEP_HEADER				':'
#define MIN_HTTP_LEN				18 //"GET / HTTP/1.1\r\n\r\n"

END_FS_NAMESPACE

#endif
