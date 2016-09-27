
#ifndef __SHA1_H__
#define __SHA1_H__

#include "sha1.h"

class SHA_1:public CSHA1
{
	public:
		SHA_1(){}
		~SHA_1(){}
		void Reback(unsigned char* p, unsigned int* state, unsigned int len);
		void GetBack(unsigned char* bk);
		void ReBack(unsigned char* bk, unsigned int len);
};


#endif
