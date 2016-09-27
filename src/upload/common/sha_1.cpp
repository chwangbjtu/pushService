
#include "sha_1.h"


void SHA_1::Reback(unsigned char* p, unsigned int* state, unsigned int len)
{
    int i = 0;
    for (i=0; i < 20; i++)
    {
        m_digest[i] = *p++;
    }
    for (i=0; i<5; i++)
    {
        m_state[i] = *state++;
    }
    m_count[0] = (len << 3);
    m_count[1] = (len >> 29);
}

void SHA_1::GetBack(unsigned char* bk)
{
	memmove(bk, m_digest, 20);
	memmove(bk + 20, (unsigned char*)m_state, 20);
}

void SHA_1::ReBack(unsigned char* bk, unsigned int len)
{
	memmove(m_digest, bk, 20);
	memmove((unsigned char*)m_state, bk + 20, 20);
	m_count[0] = (len << 3);
	m_count[1] = (len >> 29);
}
