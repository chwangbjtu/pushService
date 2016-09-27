#include "en_interface.h"
#include <iostream>
#include "encrypt_lgsr.h"

using namespace std;

encrypt_base* g_p_encrypt_lgsr = encrypt_lgsr::instance();
 
int ftsps::getlen (unsigned char* header) 
{
	return g_p_encrypt_lgsr->getlen(header);
}

int ftsps::decrypt (unsigned char* pkt, int len) 
{
	return g_p_encrypt_lgsr->decrypt(pkt, len);
}

int ftsps::encrypt (unsigned char* pkt, int len) 
{
	encrypt_char_t* p_encrypt_char = (encrypt_char_t*)pkt;
	unsigned short c_len = 0;
	//encrypt length
	if(len < 65535)
	{
		//p_encrypt_char->_c_len = len;
		c_len = len;
	}
	else
	{
		//p_encrypt_char->_c_len = 255;
		c_len = 65535;
	}
	//p_encrypt_char->_first_c_len = (unsigned char)(c_len>>8);
	//p_encrypt_char->_second_c_len = (unsigned char)(c_len&0x00ff);
	
	return g_p_encrypt_lgsr->encrypt(pkt, len);
} 	



