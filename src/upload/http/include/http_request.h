#ifndef __HTTP_REQUEST_H
#define __HTTP_REQUEST_H
#include "http_def.h"

BEGIN_FS_NAMESPACE

class http_request
{
public:
    /*
     * @lb
     * parse *http request header* from @buf which the data length is @len
     * @param buf : date to parse
     * @param len : length of the data buffer
     * @param request : result data
     *
     * return:
     *  0 - ok , < 0 - error
     *  */
    static int parse(char* buf,const int len,request_t& request);

	/*
	*	pack the @_req to the @buff with length @len, use http post/get request format
	*@param result : data buffer packed to
    *@param *request : source data
	*return:
	*	0--success, < 0--error occured
	*/
	static int pack(const request_t& request,string& result,long long content_length = -1);

private:
    static int parse_request_line(char* buf,int len,request_t& request);
};

END_FS_NAMESPACE

#endif
