#include "http_util.h"
#include "http_def.h"
#include "k_str.h"
#ifdef _WIN32
#include <string.h>
#else
#include <string.h>
#include <strings.h>
#endif

BEGIN_FS_NAMESPACE

/*
*	split a @str by @sep, return by a vector
*/
int split(const string &str, const char sep, vector<string> &elements)
{
	int off = 0;
	size_t pos = string::npos;

	while ((pos=str.find(sep, off)) != string::npos)
	{
		string elem = str.substr(off, pos-off);

		if(elem != "")
		{//filter empty elements
			elements.push_back(elem);
		}

		off = pos+1;
	}

	string elem = str.substr(off);

	if(elem != "")
	{//filter empty elements
		elements.push_back(elem);
	}

	return 0;
}

/*
*	parse host address from url
*@param url	url include host address
*@param host out, host parsed from url
*return:
*	0--success, 1--error
*/
int parse_address(const string &url, string &host, unsigned short &port)
{
	size_t pos1 = url.find("//");
	if(pos1 == string::npos)
		return -1;

	size_t pos2 = url.find(":", pos1+2);
	if(pos2 == string::npos)
	{
		pos2 = url.find("/", pos1+2);
		port = 80;
	}
	else
	{
		size_t pos3 = url.find("/", pos2+1);
		if(pos3 == string::npos)
		{
			string str_port = url.substr(pos2+1);
			port = atoi(str_port.c_str());
		}
		else
		{
			string str_port = url.substr(pos2+1, pos3-pos2-1);
			port = atoi(str_port.c_str());
		}
	}

	if(pos2 == string::npos)
	{
		host = url.substr(pos1+2);
	}
	else
	{
		host = url.substr(pos1+2, pos2-pos1-2);
	}

	return 0;
}

/*
*	parse http get parameter from a string like:
*		key1=value1&key2=value2&...
*@param param_str	http get parameter strings
*@param len			length of the parameter string
*@param param_pairs	parameter <key, value> pairs parsed out from the input string
*return:
*	0--parse success, -1--some value error, you can chose whether ignore this error outside
*/
int parse_parameter(const char *param_str, int len, multimap<string, string> &param_pairs)
{
	if(len <= 0)
		return 0;

	//parse param
	const char *pos_param_start = param_str;
	const char *pos_equal = (const char *)memchr(pos_param_start, SEP_EQ, len);

	while (pos_equal != NULL)
	{
		const char *pos_and = (const char *)memchr(pos_equal+1, SEP_AND, len-(pos_equal-param_str+1));

		if(pos_and != NULL)
		{
			int len1 = pos_equal - pos_param_start;
			string key;

			http_escape2str(pos_param_start, len1, key);

			len1 = pos_and-pos_equal-1;
			string value;

			http_escape2str(pos_equal+1, len1, value);
			param_pairs.insert(pair<string, string>(key, value));
			pos_param_start = pos_and+1;
			pos_equal = (const char *)memchr(pos_param_start, SEP_EQ, len-(pos_param_start-param_str));
		}
		else if(pos_and == NULL)
		{
			int len1 = pos_equal-pos_param_start;
			string key;

			http_escape2str(pos_param_start, len1, key);
			len1 = len-(pos_equal-param_str+1);

			string value;
			http_escape2str(pos_equal+1, len1, value);

			param_pairs.insert(pair<string, string>(key, value));
			break;
		}
		else
			break;
	}

	return 0;
}

/*
*	parse http headers include request and response, like:
*		Accept-Encoding: gzip,deflate
*		Content-Length: 20
*		......\r\n\r\n
*@param header_str	header strings
*@param len			length of the header string include "\r\n\r\n"
*@param header_pairs	parameter <key, value> pairs parsed out from the input string
*return:
*	0--parse success, -1--some value error, you can chose whether ignore this error outside
*/
int parse_headers(const char *header_str, int len, multimap<string, string> &header_pairs)
{
	if(len <= 4)
		return -1;

	if(memcmp(header_str+(len-4), HEADER_END, 4) != 0)
	{
		cerr<<"error: missing header end tag, header: \n"<<header_str<<endl;
		return -1;
	}

	const char *pos_header_start = header_str;

	//parse headers
	const char *pos_colon = (const char *)memchr(pos_header_start, SEP_HEADER, len);
	while (pos_colon != NULL)
	{
		const char *pos_return = (const char *)memchr(pos_colon+1, '\n', len-(pos_colon-header_str+1));
		if(pos_return != NULL)
		{
			/**parse key**/
			const char *pos_s = pos_header_start;
			while((*pos_s==' '||*pos_s=='\r'||*pos_s=='\n') && pos_s<pos_colon)
				pos_s++;
			const char *pos_e = pos_colon-1;
			while((*pos_e==' '||*pos_e=='\r'||*pos_e=='\n') && pos_e>pos_s)
				pos_e--;
			string key(pos_s, pos_e-pos_s+1);

			/*parse value*/
			pos_s = pos_colon+1;
			while((*pos_s==' '||*pos_s=='\r'||*pos_s=='\n') && pos_s<pos_return)
				pos_s++;
			pos_e = pos_return;
			while((*pos_e==' '||*pos_e=='\r'||*pos_e=='\n') && pos_e>pos_s)
				pos_e--;
			string value(pos_s, pos_e-pos_s+1);

			/*add to header pairs*/
			header_pairs.insert(pair<string, string>( key, value));

			/*change the header start position*/
			pos_header_start = pos_return + 1;
			pos_colon = (const char *)memchr(pos_header_start, SEP_HEADER,len-(pos_header_start-header_str));
		}
		else
		{
			/**parse key**/
			const char *pos_s = pos_header_start;
			while((*pos_s==' '||*pos_s=='\r'||*pos_s=='\n') && pos_s<pos_colon)
				pos_s++;
			const char *pos_e = pos_colon-1;
			while((*pos_e==' '||*pos_e=='\r'||*pos_e=='\n') && pos_e>pos_s)
				pos_e--;
			string key(pos_s, pos_e-pos_s+1);
			
			/*parse value*/
			pos_s = pos_colon+1;
			while((*pos_s==' '||*pos_s=='\r'||*pos_s=='\n') && pos_s<header_str+len-1)
				pos_s++;
			pos_e = header_str+len-1;
			while((*pos_e==' '||*pos_e=='\r'||*pos_e=='\n') && pos_e>pos_s)
				pos_e--;
			string value(pos_s, pos_e-pos_s+1);

			header_pairs.insert(pair<string, string>( key, value));
			break;
		}
	}

	return 0;
}

/*
*	parse http headers include request and response, like:
*		Accept-Encoding: gzip,deflate\r\n
*		Content-Length: 20\r\n
*		\r\n
*
*	header:(from http the definitive guide.english,page 47)
*	    Zero or more headers, each of which is a name, followed by a colon (:), followed
*	    by optional whitespace, followed by a value, followed by a CRLF.
*
*	Support value has \r or \n compare with parse_headers()
*
*@param header_str	header strings
*@param len			length of the header string include "\r\n\r\n"
*@param header_pairs	parameter <key, value> pairs parsed out from the input string
*return:
*	0--parse success, -1--some value error, you can chose whether ignore this error outside
*/
#define TRIM(str,op)            do{ while( (*str == ' ') || (*str == '\r') || (*str == '\n' ) ) {op str;} } while(0)
int parse_headers_http(const char *header_str, int len, multimap<string, string> &header_pairs)
{
	if(len <= 4)
		return -1;

	if(memcmp(header_str+(len-4), HEADER_END, 4) != 0)
	{
		cerr<<"error: missing header end tag, header: \n"<<header_str<<endl;
		return -1;
	}

	const char* pos_headerline_start = header_str;
    const char* pos_headerline_end = NULL;

    const char* pos_start = NULL;
    const char* pos_end = NULL;
    const char* pos_colon = NULL;

    // XXX
    // maybe 128 is enough to hold a message header name
    string key;
    key.reserve(128); 

    //parse headers
    while( (pos_headerline_end = strstr(pos_headerline_start,SEP_LINE) ) != NULL )
    {
        // find the first colon from pos_headerline_start
        pos_colon = (const char*)memchr(pos_headerline_start,SEP_HEADER,len - (pos_headerline_start - header_str));
        if( ! pos_colon )
        {
            //no item,just break;
            break;
        }

        pos_start = pos_headerline_start;
        TRIM(pos_start,++);
        pos_end = pos_colon - 1;
        TRIM(pos_end,--);
                      
        LOWCASE(pos_start,pos_end,key);

        pos_start = pos_colon + 1;
        TRIM(pos_start,++);
        pos_end = pos_headerline_end;
        TRIM(pos_end,--);
        string value(pos_start,pos_end - pos_start + 1);

        header_pairs.insert(make_pair<string,string>(key,value));

        pos_headerline_start = pos_headerline_end + 2;
        key = "";
    }
	return 0;
}
#undef TRIM

//
// whether buffer_len is 1024,2048,or 512,the function will do the job.
//
// XXX
//  return string res need call reserve()!!!
int http_escape2str(const char * str, int len, string &res)
{
    const int buffer_len = 1024;
    res.reserve(buffer_len);

    int i=0;
    int pos = 0;
    char buf[buffer_len] = {0};
    while(i < len)
    {
        char c = *(str+i);
        if(c != '%')
        {
            *(buf+pos) = c;
            pos++;
            i++;
        }
        else
        {
            if(i < len-2)
            {
                i++;
                c = *(str+i);

                if(c>='A' && c<='F')
                    *(buf+pos) |= ((c-'A'+10)<<4);
                else if(c>='0' && c<='9')
                    *(buf+pos) |= ((c-'0')<<4);
                else if(c>='a' && c<='f')
                    *(buf+pos) |= ((c-'a'+10)<<4);
                else
                    break;

                i++;
                c = *(str+i);
                if(c>='A' && c<='F')
                    *(buf+pos) |= ((c-'A'+10));
                else if(c>='0' && c<='9')
                    *(buf+pos) |= ((c-'0'));
                else if(c>='a' && c<='f')
                    *(buf+pos) |= ((c-'a'+10));
                else
                    break;

                pos++;
                i++;
            }
            else
                break;
        }
        if( buffer_len == pos )
        {
            res.append(buf,pos);
            pos = 0;
        }
    }

    res.append(buf, pos);
    return 0;
}
END_FS_NAMESPACE
