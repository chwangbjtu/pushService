#ifndef __ENCRYPT_PROTOCOL_HEADER_H
#define __ENCRYPT_PROTOCOL_HEADER_H
#pragma pack(1)
namespace ftsps 
{



/*encryption character format*/
typedef struct encrypt_character 
{
	union
	{
		unsigned short	_random;//Random Number	
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
			unsigned char	_a_index:4;//Arithmetic Index
			unsigned char	_k_index:4;//Secret Key Index
		};
		unsigned char _ak_index;
	};
	unsigned char	_second_c_len;//Cipher text Length,no use
} encrypt_char_t;
};
using namespace ftsps;

/*standard header format*/
typedef struct fs_unified_header 
{
	union 
	{
		unsigned int		_reserved;
		encrypt_char_t		_enchar;
	};
	unsigned int	_length;
	unsigned short	_type;
	unsigned short	_version;
	unsigned short	_session_id;
	unsigned short	_check_sum;
	inline int size() 
	{ 
		return sizeof(struct fs_unified_header);
	}
} fs_unihead_t;
#pragma pack()

#endif//__ENCRYPT_PROTOCOL_HEADER_H

