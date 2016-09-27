#include <arpa/inet.h>
#include <stdio.h>
#include <iostream>

using namespace std;

#pragma pack(1)
/*encryption character format*/
typedef struct encrypt_character 
{
        union
        {
                unsigned short  _random;//Random Number
                struct
                {
                        unsigned char _ran;
                        unsigned char _first_c_len;
                };
        };
        union 
        {
                struct 
                {
                        unsigned char   _a_index:4;//Arithmetic Index
                        unsigned char   _k_index:4;//Secret Key Index
                };
                unsigned char _ak_index;
        };
        unsigned char   _second_c_len;//Cipher text Length,no use
} encrypt_char_t;
#pragma pack()

    int KEY_LEN1 = 128;
    //_sk = (unsigned char*)malloc(KEY_LEN1);
    unsigned char _sk[128];

int xor_operation(unsigned char* msg,int len)
{
    encrypt_char_t* p_encrypt_char = (encrypt_char_t*)msg;
    unsigned int key_index = p_encrypt_char->_k_index<<3;
    unsigned int rand_key = p_encrypt_char->_random;//_random is unsigned short
    unsigned char rank = p_encrypt_char->_ran;
    rank ^= p_encrypt_char->_first_c_len;
    len = len -4;
    msg = msg + 4;

    unsigned int ki = key_index;
    int j = 0;
    for (;j<len;)
    {
        for(;ki<=KEY_LEN1-1 && j<len ;)
        {
            printf("%x,",msg[j]);
             msg[j] ^= _sk[ki] ^ rank;
            printf("%x,%x,%x\n",_sk[ki],rank,msg[j]);

            ki += 1;
            j += 1;
        }
        ki = 0;
    }

    return 0;
}

int decrypt(unsigned char *pkt, int len)
{
    xor_operation((unsigned char*)(pkt),len);
    return 0;
}

int get_checksum(unsigned char *pkt, int len)
{
    unsigned short checksum1 = ntohs(*(unsigned short*)(pkt+14));
    unsigned short * pchecksum = (unsigned short*)(pkt+14);
    *pchecksum = 0;

    unsigned short checksum = *((unsigned short*)pkt);
    printf("%x,",checksum);
    for( int i=2;i<16;i = i+2)
    {
        checksum = checksum ^ *((unsigned short*)(pkt+i));
        printf("%x,",checksum);
    }
    cout<<endl;
    printf("%x,%x\n",checksum1,ntohs(checksum));
    return ntohs(checksum);
}

int printn(unsigned char* msg,int len)
{
    for(int i=0;i<len;i++)
        printf("%x,",msg[i]);
    cout<<endl;
}

int main()
{

    _sk[0] = 0xCC;_sk[1] = 0x47;_sk[2] = 0xE2;_sk[3] = 0xE6;
    _sk[4] = 0x2D;_sk[5] = 0x71;_sk[6] = 0x74;_sk[7] = 0x11;
    _sk[8] = 0x4D;_sk[9] = 0x21;_sk[10] = 0x28;_sk[11] = 0xDD;
    _sk[12] = 0xD4;_sk[13] = 0x6F;_sk[14] = 0x21;_sk[15] = 0x34;
    _sk[16] = 0xAc;_sk[17] = 0x88;_sk[18] = 0x0A;_sk[19] = 0x75;
    _sk[20] = 0x55;_sk[21] = 0x7F;_sk[22] = 0x1A;_sk[23] = 0xD4;
    _sk[24] = 0x9A;_sk[25] = 0x46;_sk[26] = 0x0A;_sk[27] = 0x65;
    _sk[28] = 0xB4;_sk[29] = 0x52;_sk[30] = 0xC4;_sk[31] = 0xC9;
    _sk[32] = 0x6C;_sk[33] = 0x99;_sk[34] = 0xBE;_sk[35] = 0x68;
    _sk[36] = 0xCF;_sk[37] = 0x77;_sk[38] = 0x06;_sk[39] = 0x60;
    _sk[40] = 0x1E;_sk[41] = 0x63;_sk[42] = 0x5F;_sk[43] = 0x3C;
    _sk[44] = 0x89;_sk[45] = 0xE1;_sk[46] = 0x7F;_sk[47] = 0x59;
    _sk[48] = 0x2E;_sk[49] = 0x98;_sk[50] = 0x0C;_sk[51] = 0x65;
    _sk[52] = 0x1D;_sk[53] = 0x36;_sk[54] = 0x56;_sk[55] = 0x58;
    _sk[56] = 0x71;_sk[57] = 0xF9;_sk[58] = 0xB6;_sk[59] = 0x28;
    _sk[60] = 0x14;_sk[61] = 0xA4;_sk[62] = 0xCA;_sk[63] = 0xA7;
    _sk[64] = 0x02;_sk[65] = 0x83;_sk[66] = 0x7A;_sk[67] = 0x90;
    _sk[68] = 0x8D;_sk[69] = 0x89;_sk[70] = 0x8B;_sk[71] = 0x13;
    _sk[72] = 0xC5;_sk[73] = 0xD4;_sk[74] = 0x13;_sk[75] = 0xEC;
    _sk[76] = 0x20;_sk[77] = 0xE1;_sk[78] = 0xEE;_sk[79] = 0xDA;
    _sk[80] = 0x98;_sk[81] = 0x82;_sk[82] = 0xD1;_sk[83] = 0x4F;
    _sk[84] = 0xB2;_sk[85] = 0x9c;_sk[86] = 0x8D;_sk[87] = 0xE4;
    _sk[88] = 0xD9;_sk[89] = 0xC1;_sk[90] = 0x97;_sk[91] = 0xAF;
    _sk[92] = 0xCD;_sk[93] = 0x8E;_sk[94] = 0xF5;_sk[95] = 0x87;
    _sk[96] = 0xAC;_sk[97] = 0x17;_sk[98] = 0x9B;_sk[99] = 0x47;
    _sk[100] = 0xE0;_sk[101] = 0x4E;_sk[102] = 0xC6;_sk[103] = 0xF1;
    _sk[104] = 0xE9;_sk[105] = 0x7C;_sk[106] = 0xA9;_sk[107] = 0x95;
    _sk[108] = 0xF1;_sk[109] = 0xF1;_sk[110] = 0x97;_sk[111] = 0xA2;
    _sk[112] = 0x1C;_sk[113] = 0xEF;_sk[114] = 0xA0;_sk[115] = 0x6C;
    _sk[116] = 0x24;_sk[117] = 0x8A;_sk[118] = 0x0F;_sk[119] = 0x7F;
    _sk[120] = 0xA6;_sk[121] = 0x82;_sk[122] = 0xF3;_sk[123] = 0xC3;
    _sk[124] = 0x4D;_sk[125] = 0x61;_sk[126] = 0xDD;_sk[127] = 0xC0;


    unsigned char data[] = {0x69,0x00,0x30,0x00,0xf3,0x2f,0x63,0x1c,
            0xc2,0x39,0xad,0xa1,0x05,0xf0,0x91,0x12};

    printn(data,16);
        
    decrypt(data,16);

    get_checksum(data,16);

    printn(data,16); 

    return 0;
}
