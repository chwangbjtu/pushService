#ifndef __RET_CODE__
#define __RET_CODE__

#include <iostream>
#include <string.h>

using namespace std;

const string sret_ok = "200";
const int iret_ok = 200;
const string sret_miss_para = "600";
const int iret_miss_para = 600;
const string sret_para_err = "601";
const int iret_para_err = 601;
const string sret_para_timeout = "602";
const int iret_para_timeout = 602;
const string sret_server_err = "603";
const int iret_server_err = 603;
const string sret_reupload_err = "604";
const int iret_reupload_err = 604;

const string sresult_ok = "0"; 
const string sresult_err = "1";

enum
{
	send_upload_begin = 1,
	send_upload_finish = 2,
	send_over = 3,
	send_transcode = 4,
	//send_over = 7
};

const string cmd_http_prog = "prog";

const string cmd_upload_start = "upload_start";
const string cmd_upload_start_path = "/maze/upload_start";
const string cmd_upload_finish = "upload_finish";
const string cmd_upload_finish_path = "/maze/upload_finish";
const string cmd_transcode_add = "transcode_add";
const string cmd_transcode_add_path = "/transcode_add";


#endif//__RET_CODE__
