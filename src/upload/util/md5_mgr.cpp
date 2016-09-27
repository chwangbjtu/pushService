#include <openssl/md5.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include "md5_mgr.h"

using namespace std;

md5_mgr* md5_mgr::_inst = NULL;
md5_mgr* md5_mgr::instance()
{
    if ( _inst == NULL)
        _inst = new md5_mgr();
    return _inst;
}

md5_mgr::md5_mgr()
{
    pthread_mutex_init(&_mutex,NULL);
}

int md5_mgr::get_md5str(string& filename,string& md5str)
{
    pthread_mutex_lock(&_mutex);
    unsigned char result[MD5_DIGEST_LENGTH];

    int file_descript = -1;
    unsigned long file_size = 0;
    char* file_buffer = NULL;

    struct stat statbuf;
    file_descript = open(filename.data(), O_RDONLY);

    if(file_descript < 0)
    {
        pthread_mutex_unlock(&_mutex);
        return -1;
    }

    if(fstat(file_descript, &statbuf) < 0)
    {
        pthread_mutex_unlock(&_mutex);
        return -1;
    }
    file_size =statbuf.st_size;

    file_buffer = (char*)mmap(0, file_size, PROT_READ, MAP_SHARED, file_descript, 0);
    MD5((unsigned char*) file_buffer, file_size, result);
    munmap(file_buffer, file_size);

    unsigned char tt [MD5_DIGEST_LENGTH*2+1];

    for(int i=0; i <MD5_DIGEST_LENGTH; i++) 
    {
            //printf("%02x",md[i]);
            sprintf((char*)(tt+i*2),"%02x",result[i]);
    }
    const char* pstr = (const char *)tt;

    md5str.assign(pstr,MD5_DIGEST_LENGTH*2);
    //md5str.append(pstr,1);

    pthread_mutex_unlock(&_mutex);

    return 0;
}
