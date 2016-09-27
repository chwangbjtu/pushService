#ifndef __HTTP_UTIL_H
#define __HTTP_UTIL_H
#include <string>
#include <vector>
#include <map>
#include <iostream>
#include "k_ns.h"

BEGIN_FS_NAMESPACE

using namespace std;

/*
 * Each header field consists of a name followed by a colon (":") and the 
 * field value. Field names are case-insensitive. 
 *  (from rfc2616 4.2 Message Headers)
 *
 *  */
// @lb for translate a string to be lowcased
#define LOWCASE(start,end,result)                  do{                                                      \
                                                            char* str_start = const_cast<char*>(start);     \
                                                            char* str_end = const_cast<char*>(end);         \
                                                            do{                                             \
                                                                int c = *str_start;                        \
                                                                 if( isupper(c) )                  \
                                                                    c = tolower(c);                \
                                                                result += c;             \
                                                            }while( str_start++ != str_end  );                 \
                                                    }while(0)



//split string by separator
int split(const string &str, const char sep, vector<string> &elements);

//parse a host or ip address from a url like: http://xxx.xxx.xxx:port/xxx?xxx=xxx&...
int parse_address(const string &url, string &host, unsigned short &port);

//parse http get parameter from a string like: key1=value1&key2=value2&...
int parse_parameter(const char *param_str, int len, multimap<string, string> &param_pairs);

//parse http get headers
int parse_headers(const char *header_str, int len, multimap<string, string> &header_pairs);

// @lb
// parse http header
int parse_headers_http(const char *header_str, int len, multimap<string, string> &header_pairs);

// decode url code,just replace for escaoe2str() in k_str.cpp(has 1024 limit)
int http_escape2str(const char * str, int len, string &res);

END_FS_NAMESPACE
#endif
