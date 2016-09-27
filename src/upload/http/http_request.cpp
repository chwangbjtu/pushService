#include <stdio.h>
#include <string.h>
#include <sstream>
#include "http_request.h"
#include "http_util.h"
#include "k_str.h"
#include "k_os.h"

BEGIN_FS_NAMESPACE

// private function, request MUST BE NOT NULL,when call it.
int http_request::parse_request_line(char* buf,int len,request_t& request)
{
    string cmd(buf,4);

    char* start = buf;
    // \r\n
    int line_length = len - 2;

    // check method and set
    if( cmd ==  "POST" )
    {
        request._method = "POST";
        start += strlen("POST") + 1;
        line_length -= strlen("POST") + 1;
    } else if( cmd == "GET " )
    {
        request._method = "GET";
        start += strlen("GET") + 1;
        line_length -= strlen("GET") + 1;
    } 
    else if (cmd == "OPTI")
    {
        request._method = "OPTIONS";
        start += strlen("OPTIONS") + 1;
        line_length -= strlen("OPTIONS") + 1;
    }
    else 
    {
        cerr << "error : get command fail" << endl;
        return -1;
    }

    // get url
    char* p = (char*)memchr(start,SEP_SPACE,line_length);
    if( !p )
    {
        cerr << "error : get url fail "  << start << endl;
        return -1;
    }

    request._path_and_parameters = string(start, p - start );
    const char *path_sep = (const char *)memchr(request._path_and_parameters.c_str(), SEP_QM, 
													request._path_and_parameters.size());
    if(path_sep == NULL)
    {//no parameters
        request._path = request._path_and_parameters;
    }
    else
    {//with parameters
        //path
        request._path = string(request._path_and_parameters.c_str(), path_sep - request._path_and_parameters.c_str());

        //parameter strings
        request._paramstr = string(path_sep+1);

        //parse parameters
        if (0 != parse_parameter(path_sep+1, strlen(path_sep+1),request._map_params))
            return -1;
    }
    
    line_length -= p - start ;
    start = p + 1;

    //find http version
    const char *version_sep = (const char *)memchr(start,
                                                   SEP_VERSION, 
                                                   line_length);
    if(version_sep != NULL)
    {
        string httpstr = string(start, version_sep-start);
        if(strcasecmp(httpstr.c_str(), "HTTP") == 0)
        {
            request._version = string(version_sep+1,line_length - (version_sep - start+ 1));
            if(request._version != "1.0" && request._version != "1.1")
            {
                cerr<<"error: unsupported http version, buf: \n"<<buf<<endl;
                return -1;
            }
        }
        else
        {
            cerr<<"error: missing http version, buf: \n"<<buf<<endl;
            return -1;
        }
    }
    else
    {
        cerr<<"error: missing http version, buf: \n"<<buf<<endl;
        return -1;
    }
    return 0;
}

int http_request::parse(char* buf,const int len,request_t& request)
{
    int reminder_len = len;
    char* line_start =  buf;
    char* line_end = strstr(line_start,SEP_LINE);
    if( !line_end )
    {
        cerr << "error :  missing request_line or state_line,buf : \n" << buf << endl;
        return -1;
    }

    //parse request_line 
    if( parse_request_line(line_start,line_end - line_start + 1,request ) )
    {
        return -1;
    }

    // \r\n
    reminder_len -= line_end - line_start + 2;
    line_start = line_end + 2;

    parse_headers_http(line_start,reminder_len,request._map_headers);

    return 0;
}

int http_request::pack(const request_t& request,string& result,long long content_length)
{
    long long real_body_length = 0;
    if( content_length > 0 )
    {
        // if argument content_length is in used, it MUST equal 
        // with _content.size()
        
        //if( content_length != request._content.size() )
		if( request._content.size() != 0 && content_length - request._content.size() != 0 )
        {
            return -1;
        }

        real_body_length =  content_length;
    }
    else
    {
        // use _content.size() when argument content_lenght is default value
        real_body_length =  request._content.size();
    }

    result.reserve(request._content.size() + 4096);

    //method and path
    result += request._method + " " + request._path;

    multimap<string, string>::const_iterator c_iter = request._map_params.begin();
    multimap<string, string>::const_iterator c_iter_end = request._map_params.end();

    //if there is parameters, add '?' after path
    if( c_iter != c_iter_end )
    {
        result += "?";

        //parameters
        string key(""), val("");
        str2escape(c_iter->first.c_str(),c_iter->first.length(), key);
        str2escape(c_iter->second.c_str(),c_iter->second.length(), val);

        result += key + "=" + val;

        ++c_iter;

        for(; c_iter != c_iter_end; ++c_iter)
        {
            str2escape(c_iter->first.c_str(),c_iter->first.length(), key);
            str2escape(c_iter->second.c_str(),c_iter->second.length(), val);

            result += "&" + key + "=" + val;
        }
    }

    //HTTP version
    result += " HTTP/" + request._version + "\r\n";

    //headers
    c_iter = request._map_headers.begin();
    c_iter_end = request._map_headers.end();
    for(; c_iter != c_iter_end; c_iter++)
    {
        // XXX
        // name: content ( message header)
        // only urlencode the content,don't encode the name
        //str2escape(c_iter->first.c_str(),c_iter->first.length(), key);
        result += c_iter->first + ": " + c_iter->second + "\r\n";
    }

    // add body's length;
    if( real_body_length > 0 )
    {
        stringstream s; 
        s << real_body_length;

        result += "Content-Length: " + s.str() + "\r\n";
        /*
        char tmp[64] = {0};
        int len = snprintf(tmp,sizeof(tmp),"%d",real_body_length );

        result += "Content-Length: " + string(tmp) + "\r\n";
        */
    }

    result += "\r\n";

    // message body
    if( request._content.size() > 0 )
    {
        result += request._content;
    }
    return 0;
}

END_FS_NAMESPACE
