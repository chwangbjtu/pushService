#include <stdlib.h>
#include <sstream>
#include <arpa/inet.h>
#include <string>
#include "json/json.h"
#include "dbg.h"
#include "util.h"
#include "msg_mgr.h"
#include "user_mgr.h"
#include "proto_constant.h"
#include "proto_process.h"
#include "fp_login_req_v1_handler.h"
#include "tlogger.h"

using namespace std;

int fp_login_req_v1_handler::process(string& req,unsigned int ip,int threadid,int& id,string& rtoken,string& resp)
{
    const char* s = req.data();
    //int length = ntohl(*((unsigned int*)(s+proto_header_length_offset)));
    header_struct_t * p_req = (header_struct_t *)(req.data());
    if ( req.size() < p_req->size())
    {
        tlogger::instance()->log("loginp",fsk::level_t::debug_level(),rtoken,1,1);
        return -1;
    }

    int length = ntohl(p_req->_length);

    string sjson;
    //if ( length + proto_header_len < req.size())
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
    else
    {
    }
    
    string fudid;
    string key = "token";//fudid
    Json::Reader reader(Json::Features::strictMode());
    Json::Value value;
    if ( reader.parse(sjson,value))
    {
        if ( value.isMember(key) && !value[key].isNull()
                    && value[key].isString())
        {
            fudid = value[key].asString();
            if ( rtoken.size() == 0)
            {
                rtoken = fudid;
            }
        }
    }
    else
    {
        tlogger::instance()->log("loginp",fsk::level_t::debug_level(),rtoken,2,1);
        return -1;
    }

    string sapp_name = "app_name";//app_name
    string app_name;
    if ( value.isMember(sapp_name) && !value[sapp_name].isNull()
                    && value[sapp_name].isString())
    {
        app_name = value[sapp_name].asString();
    }
    int app_id = -1;
    app_id = util::instance()->get_app_id(app_name);

    string sversion = "version";//version
    string version;
    unsigned int iversion = 0;
    if ( value.isMember(sversion) && !value[sversion].isNull()
                    && value[sversion].isString())
    {
        version = value[sversion].asString();
    }
    util::instance()->str2ip(version,iversion);
    
    string slast_msg_id = "last_msg_id";
    string last_msg_id;
    if ( value.isMember(slast_msg_id) && !value[slast_msg_id].isNull()
                    && value[slast_msg_id].isString())
    {
        last_msg_id = value[slast_msg_id].asString();
    }

    if ( fudid.size() == 0 || app_id == -1 || iversion <= 0)
    {
        string tstr = app_name;
        tstr.append(",");
        tstr.append(version);
        tlogger::instance()->log("loginp",fsk::level_t::debug_level(),rtoken,tstr,1);
        tlogger::instance()->log("loginp",fsk::level_t::debug_level(),rtoken,3,1);
        return -1;
    }
    
    user_mgr::instance()->login(threadid,id,fudid,app_id,iversion,ip);
    
    if(!last_msg_id.empty()) {
        int last_msg_id_int = atoi(last_msg_id.c_str());
        int newest_msgid = msg_mgr::instance()->get_newest_msgid(last_msg_id_int, app_id);
        if (newest_msgid > 0) {
            user_mgr::instance()->push_msg(fudid, newest_msgid, 0);
        }
    }
    
    proto_login::pack_resp_v1(resp);
	return 0;
}

