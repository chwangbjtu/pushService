# -*-coding:utf-8 -*- 
import struct
import random

#msg head 
rand_key_start = 0
ak_index_start = 2
length_start = 4
type_start = 8
version_start = 10
sid_start = 12
check_num_start = 14
msg_head_length = 16

#type
proto_login_req = 0x1001
proto_login_resp = 0x1f01
proto_htbt_req = 0x1002
proto_htbt_resp = 0x1f02
proto_push_req = 0x1003
proto_push_resp = 0x1f03

#secret_key
secret_key_length = 128
secret_key = [
      0xCC,  0x47,  0xE2,  0xE6,
      0x2D,  0x71,  0x74,  0x11,
      0x4D,  0x21,  0x28,  0xDD,
      0xD4,  0x6F,  0x21,  0x34,
      0xAc,  0x88,  0x0A,  0x75,
      0x55,  0x7F,  0x1A,  0xD4,
      0x9A,  0x46,  0x0A,  0x65,
      0xB4,  0x52,  0xC4,  0xC9,
      0x6C,  0x99,  0xBE,  0x68,
      0xCF,  0x77,  0x06,  0x60,
      0x1E,  0x63,  0x5F,  0x3C,
      0x89,  0xE1,  0x7F,  0x59,
      0x2E,  0x98,  0x0C,  0x65,
      0x1D,  0x36,  0x56,  0x58,
      0x71,  0xF9,  0xB6,  0x28,
      0x14,  0xA4,  0xCA,  0xA7,
      0x02,  0x83,  0x7A,  0x90,
      0x8D,  0x89,  0x8B,  0x13,
      0xC5,  0xD4,  0x13,  0xEC,
      0x20,  0xE1,  0xEE,  0xDA,
      0x98,  0x82,  0xD1,  0x4F,
      0xB2,  0x9c,  0x8D,  0xE4,
      0xD9,  0xC1,  0x97,  0xAF,
      0xCD,  0x8E,  0xF5,  0x87,
      0xAC,  0x17,  0x9B,  0x47,
      0xE0,  0x4E,  0xC6,  0xF1,
      0xE9,  0x7C,  0xA9,  0x95,
      0xF1,  0xF1,  0x97,  0xA2,
      0x1C,  0xEF,  0xA0,  0x6C,
      0x24,  0x8A,  0x0F,  0x7F,
      0xA6,  0x82,  0xF3,  0xC3,
      0x4D,  0x61,  0xDD,  0xC0
              ]

def parse_msg(msg):
    result = {}
    length = len(msg)
    #check length
    if length < msg_head_length:
        return None
    
    #get random key and ak index
    result = parse_msg_head(msg[0:msg_head_length])
    if not result:
        return None
    
    # decrypt
    if length >= msg_head_length:
        decrypt_str = xor_operation(result['k_index'], result['random_key'], msg, result['length'])
    
        # check checknum
        your_check_num, = struct.unpack("!H",decrypt_str[check_num_start:msg_head_length])
        my_check_num = get_checksum(decrypt_str[0:check_num_start])
        if your_check_num != my_check_num:
            return None
        
        # get type, source msg
        type, = struct.unpack("!H",decrypt_str[type_start:version_start])
        source = decrypt_str[msg_head_length:]
        result['type'] = type
        result['source'] = source
    return result
    
    
def build_msg(type, msg):
    random_key = random.randint(0, 65535) & 0xffff
    k_index = random.randint(0, 15)
    a_index = 0
    ak_index = (k_index & 0x0f) << 4 | a_index
    reserved = 0
    version = 0x0001
    sid = 0x1234
    length = len(msg) + msg_head_length
    
    head_str = struct.pack('!HBBIHHH', random_key, ak_index, reserved, length, type, version, sid)
    check_num = get_checksum(head_str)
    format = '!%dsH' % (check_num_start)
    head_str = struct.pack(format, head_str, check_num)
    msg = head_str + msg
    return xor_operation(k_index, random_key, msg, length)
    
def parse_msg_head(head):
    random_ak = head[0:length_start]
    result = {}
    format = '!HBB'
    random_key,ak_index,reserved = struct.unpack(format, random_ak)
    result['random_key'] = random_key
    #Big-Endian
    k_index = (ak_index & 0xf0) >> 4
    a_index = ak_index & 0x0f
    length = get_length(k_index, random_key, head)
    result['a_index'] = a_index
    result['k_index'] = k_index
    result['length'] = length
    return result
    
def get_checksum(msg):
    ret = struct.unpack('!HHHHHHH', msg)
    check_num = ret[0]
    for i in ret[1:]:
        check_num = check_num ^ i
    return check_num
    
def get_length(k_index, random_key, head):
    length_str = head[length_start:type_start]
    key_index = k_index << 3
    rank = (random_key & 0x00ff) ^ ((random_key & 0xff00) >> 8) 
    ki = key_index
    final = '' 
    for i in length_str:
        tmp_msg = ord(i)
        tmp_msg = tmp_msg ^ secret_key[ki] ^ rank
        final += chr(tmp_msg)
        ki += 1
        
    length, = struct.unpack("!I", final)
    return length
    
def xor_operation(k_index, random_key, msg, length):
    key_index = k_index << 3
    rank = (random_key & 0x00ff) ^ ((random_key & 0xff00) >> 8)
    final_msg = msg[0:4]
    msg = msg[4:length]
    length = length - 4
    j = 0
    ki = key_index
    while j < length:
        while ki <= secret_key_length - 1 and j < length:
            tmp_msg = ord(msg[j])
            tmp_msg = tmp_msg ^ secret_key[ki] ^ rank
            final_msg += chr(tmp_msg)
            ki += 1
            j += 1
        ki = 0
    return final_msg
    
if __name__ == '__main__':
    source = "hello world"
    dest = build_msg(proto_login_req, source)
    print parse_msg(dest)
    