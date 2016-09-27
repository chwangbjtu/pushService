#ifndef __MD5_MGR_H
#define __MD5_MGR_H

#include <pthread.h>
#include <string>

using namespace std;

class md5_mgr
{
public:
    ~md5_mgr();

    static md5_mgr* instance();
    
    int get_md5str(string& filename,string& md5str);
private:
    md5_mgr();

    static md5_mgr* _inst;
    pthread_mutex_t _mutex;
};

#endif//__MD5_MGR_H


