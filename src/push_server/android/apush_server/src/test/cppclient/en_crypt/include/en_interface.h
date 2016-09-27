#ifndef __I_ENCRYPTION_H
#define __I_ENCRYPTION_H

#include "stdio.h"
namespace ftsps 
{
	/*
	*	get package' length from crypttext
	*@param pkt : pointer of the package buffer
	*@param len : length of the package buffer
	*return:
	*	this function shall return the length package. 
	*	return <=0 indicate an  error.
	*/
	int getlen (unsigned char* header);

	/*
	*	decrypt package buffer
	*@param pkt : pointer of the package buffer
	*@param len : length of the package buffer
	*return:
	*	this function shall return the length plaintext, and length crypttext msut be >=16. 
	*	return <=0 indicate an  error.
	*/
	int decrypt (unsigned char* pkt, int len);

	/*
	*	encrypt package buffer
	*@param pkt : pointer of the package buffer
	*@param len : length of the package buffer
	*return:
	*	this function shall return the length crypttext, and length crypttext msut be >=16. 
	*	return <=0 indicate an  error.
	*/
	int encrypt (unsigned char* pkt, int len);
};
using namespace ftsps;
#endif//__I_ENCRYPTION_H

