#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <string>
#include "encrypt_lgsr.h"

using namespace std;

encrypt_lgsr* encrypt_lgsr::_inst = NULL;
encrypt_lgsr* encrypt_lgsr::instance()
{
	if ( _inst == NULL)
	{
		_inst = new encrypt_lgsr();
	}
	return _inst;
}


encrypt_lgsr::encrypt_lgsr()
{
	_algsr1 = new arithmetic1_lgsr();
	
	int idx = 0;//encrypt algorithm index 0
	this->register_arithmetic(idx,_algsr1);

}

encrypt_lgsr::~encrypt_lgsr(){}


//for arith_lgsr
arithmetic1_lgsr::arithmetic1_lgsr()
{
    KEY_LEN1 = 128;

    KEY_LEN1 = 128;
    _secret_key = (unsigned char*)malloc(KEY_LEN1);
    _secret_key[0] = 0xCC;_secret_key[1] = 0x47;_secret_key[2] = 0xE2;_secret_key[3] = 0xE6;
    _secret_key[4] = 0x2D;_secret_key[5] = 0x71;_secret_key[6] = 0x74;_secret_key[7] = 0x11;
    _secret_key[8] = 0x4D;_secret_key[9] = 0x21;_secret_key[10] = 0x28;_secret_key[11] = 0xDD;
    _secret_key[12] = 0xD4;_secret_key[13] = 0x6F;_secret_key[14] = 0x21;_secret_key[15] = 0x34;
    _secret_key[16] = 0xAc;_secret_key[17] = 0x88;_secret_key[18] = 0x0A;_secret_key[19] = 0x75;
    _secret_key[20] = 0x55;_secret_key[21] = 0x7F;_secret_key[22] = 0x1A;_secret_key[23] = 0xD4;
    _secret_key[24] = 0x9A;_secret_key[25] = 0x46;_secret_key[26] = 0x0A;_secret_key[27] = 0x65;
    _secret_key[28] = 0xB4;_secret_key[29] = 0x52;_secret_key[30] = 0xC4;_secret_key[31] = 0xC9;
    _secret_key[32] = 0x6C;_secret_key[33] = 0x99;_secret_key[34] = 0xBE;_secret_key[35] = 0x68;
    _secret_key[36] = 0xCF;_secret_key[37] = 0x77;_secret_key[38] = 0x06;_secret_key[39] = 0x60;
    _secret_key[40] = 0x1E;_secret_key[41] = 0x63;_secret_key[42] = 0x5F;_secret_key[43] = 0x3C;
    _secret_key[44] = 0x89;_secret_key[45] = 0xE1;_secret_key[46] = 0x7F;_secret_key[47] = 0x59;
    _secret_key[48] = 0x2E;_secret_key[49] = 0x98;_secret_key[50] = 0x0C;_secret_key[51] = 0x65;
    _secret_key[52] = 0x1D;_secret_key[53] = 0x36;_secret_key[54] = 0x56;_secret_key[55] = 0x58;
    _secret_key[56] = 0x71;_secret_key[57] = 0xF9;_secret_key[58] = 0xB6;_secret_key[59] = 0x28;
    _secret_key[60] = 0x14;_secret_key[61] = 0xA4;_secret_key[62] = 0xCA;_secret_key[63] = 0xA7;
    _secret_key[64] = 0x02;_secret_key[65] = 0x83;_secret_key[66] = 0x7A;_secret_key[67] = 0x90;
    _secret_key[68] = 0x8D;_secret_key[69] = 0x89;_secret_key[70] = 0x8B;_secret_key[71] = 0x13;
    _secret_key[72] = 0xC5;_secret_key[73] = 0xD4;_secret_key[74] = 0x13;_secret_key[75] = 0xEC;
    _secret_key[76] = 0x20;_secret_key[77] = 0xE1;_secret_key[78] = 0xEE;_secret_key[79] = 0xDA;
    _secret_key[80] = 0x98;_secret_key[81] = 0x82;_secret_key[82] = 0xD1;_secret_key[83] = 0x4F;
    _secret_key[84] = 0xB2;_secret_key[85] = 0x9c;_secret_key[86] = 0x8D;_secret_key[87] = 0xE4;
    _secret_key[88] = 0xD9;_secret_key[89] = 0xC1;_secret_key[90] = 0x97;_secret_key[91] = 0xAF;
    _secret_key[92] = 0xCD;_secret_key[93] = 0x8E;_secret_key[94] = 0xF5;_secret_key[95] = 0x87;
    _secret_key[96] = 0xAC;_secret_key[97] = 0x17;_secret_key[98] = 0x9B;_secret_key[99] = 0x47;
    _secret_key[100] = 0xE0;_secret_key[101] = 0x4E;_secret_key[102] = 0xC6;_secret_key[103] = 0xF1;
    _secret_key[104] = 0xE9;_secret_key[105] = 0x7C;_secret_key[106] = 0xA9;_secret_key[107] = 0x95;
    _secret_key[108] = 0xF1;_secret_key[109] = 0xF1;_secret_key[110] = 0x97;_secret_key[111] = 0xA2;
    _secret_key[112] = 0x1C;_secret_key[113] = 0xEF;_secret_key[114] = 0xA0;_secret_key[115] = 0x6C;
    _secret_key[116] = 0x24;_secret_key[117] = 0x8A;_secret_key[118] = 0x0F;_secret_key[119] = 0x7F;
    _secret_key[120] = 0xA6;_secret_key[121] = 0x82;_secret_key[122] = 0xF3;_secret_key[123] = 0xC3;
    _secret_key[124] = 0x4D;_secret_key[125] = 0x61;_secret_key[126] = 0xDD;_secret_key[127] = 0xC0;

}

arithmetic1_lgsr::~arithmetic1_lgsr(){}

int arithmetic1_lgsr::printn(unsigned char* header,int len)
{
    cout<<endl;
    for(int i=0;i<len;i++)
    {
        cout<<endl;
    }
    return 0;
}


int arithmetic1_lgsr::getlen(unsigned char* header)
{
	encrypt_char_t* p_encrypt_char = (encrypt_char_t*)header;
	//unsigned int key = p_encrypt_char->_random ^ _ckey[p_encrypt_char->_k_index];
	unsigned int key_index = p_encrypt_char->_k_index<<3;
    unsigned char rank = p_encrypt_char->_ran;
    rank ^= p_encrypt_char->_first_c_len;
    //unsigned int rand_key = p_encrypt_char->_random;//_random is unsigned short
    //unsigned short rand_key1 = ntohs(p_encrypt_char->_random);//_random is unsigned short
    //rand_key = (rand_key<<16)|rand_key;
    //unsigned char * _pkey  = (unsigned char*)_secret_key;

    unsigned char tdata[4];


    int len = -1;

    int j = 4;
    memcpy(tdata,header+4,4);
    //p_encrypt_char->_k_index只有4位，最大只能取值到15，左移3位（就是乘以8）后最大只能是120
    //不会超过127个的密钥
    //(*(unsigned short*)(&msg[j])) ^= (*(unsigned short*)(&_secret_key[ki])) ^ rand_key;//no use
    //len = (*(unsigned int*)(&header[j])) ^ ( (*(unsigned int*)(&_secret_key[key_index])) ^ rand_key );
    unsigned tlen = 0;
    j = 0;
    for(;j<4;j++,key_index++)
    {
        tdata[j] ^= _secret_key[key_index] ^ rank;
    }
    unsigned int *plen = (unsigned int *)(tdata);

	return *plen;
}

int arithmetic1_lgsr::encrypt(unsigned char *pkt, int len)
{
    if ( len < 16)
    {
        cerr<<"arithmetic1_lgsr::encrypt len < 16"<<endl;
        return -1;
    }

    unsigned short * pchecksum = (unsigned short*)(pkt+14);
    *pchecksum = 0;
    unsigned short checksum = get_checksum(pkt,len);
    *pchecksum = htons(checksum);


    xor_operation((unsigned char*)(pkt),len);
	return len;//success
}

int arithmetic1_lgsr::decrypt(unsigned char *pkt, int len)
{
    if ( len < 16)
    {
        return -1;
    }
  
     

    xor_operation((unsigned char*)(pkt),len);


    unsigned short checksum = ntohs(*(unsigned short*)(pkt+14));
    unsigned short * pchecksum = (unsigned short*)(pkt+14);
    *pchecksum = 0;
    unsigned short tchecksum = get_checksum(pkt,len);
    if ( checksum != tchecksum)
    {
        return -2;
    }

    return 0;
	
	//return p_encrypt_char->_second_c_len;//success
}

int arithmetic1_lgsr::get_checksum(unsigned char *pkt, int len)
{
    if ( len < 16)
    {
        return -1;
    }

    unsigned short checksum = *((unsigned short*)pkt);
    for( int i=2;i<16;i = i+2)
    {
        checksum = checksum ^ *((unsigned short*)(pkt+i));
    }

    return ntohs(checksum);
}

int arithmetic1_lgsr::xor_operation(unsigned char* msg,int len)
{
	//为了能够寻址到所有的key，
	//_k_index只有4位，最大只能表示16，密钥有128个；只有乘以8,才能寻址到128 
	//arithmetic index
	encrypt_char_t* p_encrypt_char = (encrypt_char_t*)msg;
    unsigned int key_index = p_encrypt_char->_k_index<<3; 
    unsigned int rand_key = p_encrypt_char->_random;//_random is unsigned short
    unsigned char rank = p_encrypt_char->_ran;
    rank ^= p_encrypt_char->_first_c_len;


    len = len -4;
    msg = msg + 4;

    unsigned int ki = key_index;
    int j = 0;//用户数据的索引
    for (;j<len;)
    {
        for(;ki<=KEY_LEN1-1 && j<len ;)
        {
            msg[j] ^= _secret_key[ki] ^ rank;
            
            ki += 1;
            j += 1;
        }
        //ki（key的索引超过128之后再从0开始）
        ki = 0;
    }

	return 0;
}


