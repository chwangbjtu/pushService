#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sstream>
#include "k_os.h"
#include "compress.h"
#include "http_response.h"
#include "http_util.h"

BEGIN_FS_NAMESPACE

int http_response::pack(response_t& resp,string& strbuf,bool is_gzip)
{
    // for compress;
    char *content_buf = NULL;
    kt::u_long content_buf_len = 0;
    stringstream size;

    int content_length = resp._content.size();
    strbuf.reserve(content_length + 4096);

    // statue line
    strbuf += "HTTP/" + resp._version + " "
        + resp._code + " " + resp._code_info + "\r\n";

    // handle message body
    if( is_gzip ) 
    {
        content_buf_len = resp._content.size()+64;
		content_buf = new char[content_buf_len];
		int zip_res = gzip((u_char*)content_buf, 
							&content_buf_len, 
							(u_char*)resp._content.c_str(), 
							content_length);

		if(zip_res != Z_OK)
		{   //zip failed, use original content
			//free the content zip buffer first
			delete content_buf;
            content_buf = NULL;
            size << content_length;
        }
        else
        {
            size << content_buf_len;
            strbuf += "Content-Encoding: gzip \r\n";
        }
    }
    else
    {
        size << content_length;
    }
    strbuf += "Content-Length: " + size.str() + "\r\n";

    // message header
    if( resp._map_headers.size() )
    {
        multimap<string,string>::const_iterator it = resp._map_headers.begin(),
            it_end = resp._map_headers.end();
        for(; it != it_end ; ++it )
        {
            strbuf += it->first + ": " + it->second + "\r\n";
        }
    }

    strbuf += "\r\n";

    // message body
    if( content_buf != NULL )
    {
        strbuf.append(content_buf,content_buf_len);
        delete content_buf;
    }
    else
    {
        strbuf.append(resp._content);
    }
    return 0;
}

int http_response::parse(const char *buf, const int len, response_t& resp)
{
    const char *pos_header_end = strstr(buf, "\r\n\r\n");
    if(pos_header_end == NULL)
    {//can not find header end separator, error package
        cerr<<"error: can not find http response header end separator, buf: \n"<<buf<<endl;
        return -1;
    }

    //find first line end separator
    const char *first_line_sep = strstr(buf, SEP_LINE);
    if(first_line_sep == NULL)
    {
        cerr<<"error: missing http protocol version, response code and information, buf: \n"<<buf<<endl;
        return -1;
    }

    //find http protocol version
    const char *pos_protocol_end = (const char *)memchr(buf, SEP_SPACE, first_line_sep-buf);
    if(pos_protocol_end == NULL)
    {
        cerr<<"error: missing http protocol version, buf: \n"<<buf<<endl;
        return -1;
    }
    const char *pos_version_sep = (const char *)memchr(buf, SEP_VERSION, pos_protocol_end-buf);
    if(pos_version_sep != NULL)
    {
        string httpstr = string(buf, pos_version_sep-buf);
        if(strcasecmp(httpstr.c_str(), "HTTP") == 0)
        {
            resp._version = string(pos_version_sep+1, pos_protocol_end-pos_version_sep-1);
            if(resp._version != "1.0" && resp._version != "1.1")
            {
                cerr<<"error: unsupported http version, buf: \n"<<buf<<endl;
                return -1;
            }
        }
        else
        {
            cerr<<"error: missing http protocol version, buf: \n"<<buf<<endl;
            return -1;
        }
    }
    else
    {
        cerr<<"error: missing http protocol version, buf: \n"<<buf<<endl;
        return -1;
    }

    //find response code
    const char *pos_code_end = (const char *)memchr(pos_protocol_end+1, SEP_SPACE, first_line_sep-pos_protocol_end-1);
    if(pos_code_end == NULL)
    {
        cerr<<"error: missing response code, buf: \n"<<buf<<endl;
        return -1;
    }
    resp._code = string(pos_protocol_end+1, pos_code_end-pos_protocol_end-1);

    //find response info
    resp._code_info = string(pos_code_end+1, first_line_sep-pos_code_end-1);

    //parse response headers
    parse_headers_http(first_line_sep+2, 
                  (int)(pos_header_end-first_line_sep+2), 
                  resp._map_headers);

    //content start pointer and length
    const char *p_content = pos_header_end+4;
    kt::u_long content_len = (kt::u_long)(len-(pos_header_end-buf+4));

    //check the content length
    multimap<string, string>::const_iterator c_iter = resp._map_headers.find("Content-Length");
    multimap<string, string>::const_iterator c_iter_end = resp._map_headers.end();
    if(c_iter != c_iter_end )
    {
        kt::u_long len = atol(c_iter->second.c_str());
        if(len != content_len)
        {//content length is not match the actual size
            return -1;
        }
    }

    //find Content-Encoding
    c_iter = resp._map_headers.find("Content-Encoding");
    if(c_iter != c_iter_end )
    {
        if((strstr(c_iter->second.c_str(), "gzip") != NULL 
            || strstr(c_iter->second.c_str(), "deflate") != NULL) 
           && content_len > 0)
        {//decompress the content
            //first 3 times of the zipped data size
            kt::u_long buf_len = 3*content_len;
            kt::byte *content_buf = new kt::byte[buf_len];

            int zip_res = un_gzip(content_buf, &buf_len, (u_char*)p_content, content_len);
            while(zip_res == Z_BUF_ERROR)
            {//buffer is too small for unzip the compressed content
                buf_len += content_len; //increase the content buffer length by content_len
                content_buf = (u_char*)realloc(content_buf, buf_len);
                zip_res = un_gzip(content_buf, 
                                      &buf_len, 
                                      (u_char*)p_content, 
                                      content_len);
            }

            if(zip_res == Z_OK)
            {
                delete content_buf; //do not forget free the buffer
                resp._content = string((char*)content_buf, buf_len);
            }
            else
            {
                delete content_buf; //do not forget free the buffer
                return -1;
            }
        }
        else //unsupported content encoding
            return -1;
    }
    else //content is not zipped
        resp._content = string(p_content, content_len);

    return 0;
}

END_FS_NAMESPACE
