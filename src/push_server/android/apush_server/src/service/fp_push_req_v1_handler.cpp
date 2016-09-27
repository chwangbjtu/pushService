#include <arpa/inet.h>
#include <stdlib.h>
#include <sstream>
#include <string>
#include "json/json.h"
#include "dbg.h"
#include "proto_constant.h"
#include "proto_process.h"
#include "fp_push_req_v1_handler.h"
#include "user_mgr.h"
#include "msg_cnt_mgr.h"
#include "tlogger.h"
#include "util.h"

int fp_push_req_v1_handler::process(string& req,unsigned int ip,int threadid,int& id,string& token,string& resp)
{
    const char* s = req.data();
    header_struct_t * p_req = (header_struct_t *)(req.data());
    if ( req.size() < p_req->size())
    {
        tlogger::instance()->log("pushp",fsk::level_t::debug_level(),token,1,1);
        return -1;
    }
    int length = ntohl(p_req->_length);

    string sjson;
    if ( length < req.size())
    {
        sjson = req.substr(proto_header_len,length);
        string treq = req.substr(length);
        req = treq;
    }
    else if (length == req.size())
    {
        sjson = req.substr(proto_header_len,length);
        req.clear();
    }

    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, sjson: %s", util::get_conn_id(threadid, id),  token.c_str(), sjson.c_str());
    Json::Reader reader(Json::Features::strictMode());
    Json::Value value;
    string msgid;
    int imsgid = -1;
    string key = "msgid";
    if ( reader.parse(sjson,value))
    {
        if ( value.isMember(key) && !value[key].isNull()
                    && value[key].isInt())
        {
            imsgid = value[key].asInt();
            stringstream os;
            os << imsgid;
            msgid = os.str();
            tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: parse json success, imsgid: %d", util::get_conn_id(threadid, id), token.c_str(), imsgid);
        }
    }
    else
    {
        tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: parse json failed", util::get_conn_id(threadid, id), token.c_str());
        tlogger::instance()->log("pushp",fsk::level_t::debug_level(),token,2,1);
        return -1;
    }

    if ( imsgid <= 0)
    {
        tlogger::instance()->log("pushp",fsk::level_t::debug_level(),token,3,1);
        return -1;
    }
    
    
    tlogger::instance()->mlog(fsk::level_t::debug_level(), "conn: %lld, token: %s, action: start erase msg", util::get_conn_id(threadid, id), token.c_str());
    int appid = -1;
	user_mgr::instance()->erase_msg(threadid,id,atoi(msgid.data()),appid);
    //if ( appid != -1 && msgid != -1)
    if ( msgid.size() > 0)
    {
	    msg_cnt_mgr::instance()->incr(appid,atoi(msgid.data()));
    }
	

	return 0;
}

