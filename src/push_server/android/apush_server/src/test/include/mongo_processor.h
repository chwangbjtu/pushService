#ifndef _MONGO_PROCESSOR_H
#define _MONGO_PROCESSOR_H

#include "client/dbclient.h"
//#include "dbclient.h"

using namespace std;

class mongo_processor
{
public:
    mongo_processor(void);
    virtual ~mongo_processor(void);

    virtual int init();
private:
    /*
    int get_nesting_obj(const char* key,const mongo::BSONObj& obj,map<int,int>& maps);    
        int get_nesting_obj(const char* key,const mongo::BSONObj& obj,map<int,int>& maps,map<int,int>& alls);
    int get_nesting_obj(int value,const char* key,const mongo::BSONObj& obj,set<int>& sets,map<int,int>& alls);
    int get_freq_value(const char* key,const mongo::BSONObj& obj,history_rec* phr);
    int get_freq_value(const char* key,const mongo::BSONObj& obj,user_data* ud);
    int get_array(const char* key,const mongo::BSONObj& obj,set<int>& sets);
    int build_nesting_obj(const map<int,int>& maps,mongo::BSONObj& obj);
    int build_array(const set<int>& sets,mongo::BSONArray& arrobj);
    int build_nesting_obj(map<string,pair<map<string,float>,map<string,vector<int> > > >& maps,mongo::BSONObj& obj);
    int build_array(const vector<int>& vectors,mongo::BSONArray& arrobj);

    //std::vector<mongo::DBClientConnection*> _online_ins;
    unsigned int _conn_num;
    */
};
#endif

