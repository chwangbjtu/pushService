#ifndef __ENCRYPT_BASE_H
#define __ENCRYPT_BASE_H

#include <stdio.h>

namespace ftsps 
{

class arithmetic_base {
	friend class encrypt_base;
protected:
	virtual int getlen (unsigned char* header) = 0;
	virtual int decrypt(unsigned char* pkt, int len) = 0;
	virtual int encrypt(unsigned char* pkt, int len) = 0; 
public:
	arithmetic_base(){}
	virtual ~arithmetic_base(){}
};

class encrypt_base  {
protected:
	arithmetic_base*	_arithmetic[16];	
	bool check_sum(unsigned short* pkt, int len);
public:
	encrypt_base():_arith_idx(1){for(int i=0;i<16;++i)_arithmetic[i]=NULL;}
	virtual ~encrypt_base(){}

	int register_arithmetic(int index, arithmetic_base* arith);	
	virtual int getlen (unsigned char* header); 
	virtual int decrypt (unsigned char* pkt, int len); 
	virtual int encrypt (unsigned char* pkt, int len); 	
private:
	char _arith_idx;
};

};
using namespace ftsps;
#endif//__ENCRYPT_BASE_H


