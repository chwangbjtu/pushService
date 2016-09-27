#ifndef __HTTP_RESPONSE_H
#define __HTTP_RESPONSE_H
#include "http_def.h"

BEGIN_FS_NAMESPACE

class http_response
{
public:
    /*
     * pack the @_resp to the string buffer @strbuf
     * pack_resp() will prealloc memory for strbuf,size is _content.size() + 4096.
     * so before call it,don't prealloc memory or prealloc memory big enough.Except 
     * compressing,other operate copy the data one time.
     *  return :
     *  0 - success , other - failed
     *
     *  */
    static int pack(response_t& resp,string& strbuf,bool gzip = false);

	/*
	*	parse http response from @buf which the data length is @len
	*@param buf : data to parse
	*@param len : length of data buffer
	*return:
	*	0--success, < 0--error occured
	*/
	static int parse(const char *buf, const int len,response_t& resp);
};

END_FS_NAMESPACE
#endif
