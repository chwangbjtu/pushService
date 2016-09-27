#include <iostream>
#include <arpa/inet.h>
#include <string.h>
#include <stdlib.h>
#include "encrypt_base.h"
#include "encrypt_protocol_header.h"

using namespace std;

int encrypt_base::register_arithmetic(int index, arithmetic_base* arith) 
{
	if ( index & 0xFFFFFFF0) 
	{
		return -1;
	}
	if ( !_arithmetic[index] && arith ) 
	{
		_arithmetic[index] = arith;
		return 0;	
	} 
	return -2;
}

int encrypt_base::getlen (unsigned char* header) 
{
	/*unpack encryption character*/
	encrypt_char_t* p_encrypt_char = (encrypt_char_t*)header;
	
	/*get length*/
	if ( !_arithmetic[p_encrypt_char->_a_index] ) 
	{
		return -1;
	} 
	else 
	{
		_arith_idx = p_encrypt_char->_a_index;
		return ntohl( _arithmetic[p_encrypt_char->_a_index]->getlen(header) );
	}
}

int encrypt_base::decrypt (unsigned char* pkt, int len) 
{
	/*check*/
	if ( !(len & 0xFFFFFFF0) ) 
	{
		return -1; 
	} 

	/*unpack encryption character*/
	encrypt_char_t* p_encrypt_char = (encrypt_char_t*)pkt;

	/*check*/
	if ( !_arithmetic[p_encrypt_char->_a_index] ) 
	{ 
		return -1; 
	} 
	
	/*decryption*/
	int ret = _arithmetic[p_encrypt_char->_a_index]->decrypt(pkt, len);

	/*check_sum*/
    /*
	int c_len = 0;
	if ( p_encrypt_char->_a_index == 2)
	{
		c_len = p_encrypt_char->_first_c_len;
		c_len = c_len << 8 | p_encrypt_char->_second_c_len;
	}
	else
	{
		c_len = p_encrypt_char->_second_c_len;
	}
	
	if ( ret && check_sum((unsigned short*)pkt, c_len) ) 
	{
		return ret;
	}
    */
    return ret;

	/*end*/
	return -1;

}

int encrypt_base::encrypt (unsigned char* pkt, int len) 
{	
	/*check*/
	if ( !(len & 0xFFFFFFF0) ) 
	{
		return -1; 
	} 

	/*unpack encryption character*/
	encrypt_char_t* p_encrypt_char = (encrypt_char_t*)pkt;


	/*check input*/
	if ( !_arithmetic[_arith_idx] ) 
	{
		return -1; 
	} 

	/*pack encryption character*/
	p_encrypt_char->_a_index = _arith_idx;
	p_encrypt_char->_ran = rand() & 0xFFFF;
	p_encrypt_char->_k_index = rand() & 0x000F; 

	/*check sum*/
	//int c_len = p_encrypt_char->_first_c_len;
	//c_len = c_len << 8 | p_encrypt_char->_second_c_len;
	//check_sum((unsigned short*)pkt, c_len);

	/*encryption*/
	return _arithmetic[p_encrypt_char->_a_index]->encrypt(pkt, len);
} 

bool encrypt_base::check_sum(unsigned short* pkt, int len)
{	
	if ( len < 16 ) return false;
	unsigned short my_check_sum = *(pkt+7);
	*(pkt+7) = 0;

	int nleft=len;
	int sum=0;
	unsigned short* temp=(unsigned short*)pkt;
	unsigned short answer=0;
	while ( nleft>1) 
	{
		sum=sum+*temp++;
		nleft=nleft-2;
	}
	if ( nleft==1)
	{
		*(unsigned char *)(&answer) = *(unsigned char *)temp;
		sum=sum+answer;
	}

	sum=(sum>>16)+(sum&0xffff);
	sum=sum+(sum>>16);
	answer=~sum;
	
	*(pkt+7) = answer;
	if ( answer == my_check_sum ) 
	{
		return true;
	} 
	else 
	{
		return false;
	}
}

