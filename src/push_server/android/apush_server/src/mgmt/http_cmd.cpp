#include <arpa/inet.h>
#include <netdb.h>
#include <vector>
#include "k_str.h"
#include "http_util.h"
#include "http_response.h"
//#include "util.h"
#include "http_cmd.h"

using namespace std;

http_cmd::http_cmd()
{
	//_return_succ = util::instance()->get_return_succ();
}

int http_cmd::pack(string& msg,string& resp)
{
	fs::http_response http_resp;
	
	http_resp._resp._content = msg;
	if(http_resp.pack(resp) < 0) 
	{
		return -1;
	}
	return 0;
}




