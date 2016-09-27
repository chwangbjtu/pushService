#ifndef __ENCRYPT_LGSR_H
#define __ENCRYPT_LGSR_H
/*encryption and decryption module */
#include "encrypt_base.h"
#include "encrypt_protocol_header.h"

class arithmetic1_lgsr:public arithmetic_base
{
public:
	arithmetic1_lgsr();
	virtual ~arithmetic1_lgsr();
	/* get encrypted msg's length fields*/
	virtual int getlen(unsigned char* header);
	/* encrypt the message begin at pkt with length len;
	 *@para[in]pkt:pointer to the message to be decrpt
	 */
	virtual int decrypt(unsigned char* pkt, int len);
	virtual int encrypt(unsigned char* pkt, int len); 
private:
	/*  xor every 4 bytes with key @key
	 *@para[in]key: encrypt/decrypt key
	 *@para[in]msg: encrypt/decrypt content
	 *@para[in]len: encrypt/decrypt content length
	*/
	int xor_operation(unsigned char* pkt,int len);

    int get_checksum(unsigned char *pkt, int len);

    int printn(unsigned char* hearder,int len);
private:
    int KEY_LEN1;
	//constant keys array
	unsigned char * _secret_key;
		
};

class encrypt_lgsr:public encrypt_base
{
public:
	virtual ~encrypt_lgsr();
	static encrypt_lgsr* instance();
private:
	encrypt_lgsr();
	static encrypt_lgsr* _inst;
	arithmetic1_lgsr* _algsr1;
};



#endif//__ENCRYPT_LGSR_H

