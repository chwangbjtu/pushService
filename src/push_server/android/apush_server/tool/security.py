# -*-coding:utf-8 -*-
#from Crypto import Random
import base64
import md5
import random
import struct
import socket
import binascii

KEY_LEN1 = 128
_secret_key = [
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


def list2str(pkt):
    res = ''
    tlen = len(pkt)
    for i in range(0,tlen):
        res = res + binascii.hexlify(chr(pkt[i]))
    return res

def str2list(pkt):
    bstr = binascii.a2b_hex(pkt)
    ts = []
    i = 0
    for i in range(0,len(bstr)):
        ts.append(ord(bstr[i]))
        i += 1
    return ts


def encrypt_xor(pkt):
    ts = str2list(pkt)
    ts1 = encrypt_xorin1(ts)
    #return ts1
    ts2 = list2str(ts1)
    return ts2


def encrypt_xorin1(pkt):
    k_index = random.randint(0, 15)
    k_index = k_index & 0x000F
    r_andom1 = random.randint(0, 65535) & 0xFF
    r_andom2 = random.randint(0, 65535) & 0xFF

    #r_andom1 = pkt[0]
    #r_andom2 = pkt[1]
    #k_index = pkt[2]>>4;

    #print hex(r_andom1),hex(r_andom2),hex(pkt[2]),hex(k_index)

    pkt[14] = 0
    pkt[15] = 0
    (tchecksum,checksum) = get_checksum(pkt,len(pkt))
    c1 = checksum >> 8
    c2 = checksum & 0x00ff
    pkt[14] = c1
    pkt[15] = c2
    
    result = xxcrypt(k_index, r_andom1,r_andom2, pkt, len(pkt))
    return result
    #return k_index, r_andom, base64.b64encode(result)

def decrypt_xor(pkt,length):
    bstr = binascii.a2b_hex(pkt)
    ts = []
    for i in range(0,len(bstr)):
        ts.append(ord(bstr[i]))

    ts1 = decrypt_xor1(ts,len(ts))
    ts2 = list2str(ts1)
    return ts2

def decrypt_xor1(pkt,length):
    #result = base64.b64decode(pkt)
    r_andom1 = int(pkt[0])
    r_andom2 = int(pkt[1])
    k_index = int(pkt[2])
    k_index = k_index >> 4
    return xxcrypt(k_index, r_andom1,r_andom2, pkt, len(pkt))

def xxcrypt(k_index, r_andom1,r_andom2, pkt, length):
    key = k_index << 3
    or1 = int(r_andom1)
    or2 = int(r_andom2)
    
    rand_key = or1 ^ or2
    i = key
    j = 0

    xxcrypt_list = [r_andom1,r_andom2,k_index<<4,0]
   
    j = 4 
    while j < length:
        while i < KEY_LEN1 and j < length:
            tmp_ord = int(pkt[j])
            tmp_ord = int(tmp_ord) ^ int(rand_key) ^ int(_secret_key[i])
            xxcrypt_list.append(tmp_ord)
            #print j,hex(pkt[j]),hex(rand_key),hex(i),hex(int(_secret_key[i])),hex(tmp_ord)
            
            i = i + 1
            j = j + 1
        i = 0

    return xxcrypt_list

def get_checksum(pkt,length):
    i = 0
    old = pkt[14] << 8 | pkt[15]
    pkt[14] = 0
    pkt[15] = 0
    tmp = 0
    while i < 16:
        tmp1 = pkt[i] << 8 | pkt[i+1]
        tmp = tmp ^ tmp1
        i += 2
        
    #print "check sum:",hex(old),hex(tmp)
    return (old,tmp)

    
def test():

    #tstr = "00010001000000787b226170705f6e616d65223a20227476222c20227469746c65223a20225c75346636305c7535393764222c20226c6173745f707573685f6964223a202232222c20226c6173745f6d73675f6964223a202232222c202276657273696f6e223a2022322e312e312e31222c20226675646964223a202237227d"
    #tstr = "0001 0001 00000078 7b226170705f6e616d65223a20227476222c20227469746c65223a20225c75346636305c7535393764222c20226c6173745f707573685f6964223a202232222c20226c6173745f6d73675f6964223a202232222c202276657273696f6e223a2022322e312e312e31222c20226675646964223a202237227d"
    #tstr = "7800 3000 00000088 1f02 0001 0000 0000 7b226170705f6e616d65223a20227476222c20227469746c65223a20225c75346636305c7535393764222c20226c6173745f707573685f6964223a202232222c20226c6173745f6d73675f6964223a202232222c202276657273696f6e223a2022322e312e312e31222c20226675646964223a202237227d"
    tstr = "78003000000000881f020001000000007b226170705f6e616d65223a20227476222c20227469746c65223a20225c75346636305c7535393764222c20226c6173745f707573685f6964223a202232222c20226c6173745f6d73675f6964223a202232222c202276657273696f6e223a2022322e312e312e31222c20226675646964223a202237227d"

    tstr = "7c0020000000008c10010001000000007b22746f6b656e223a223139322e3136382e31362e3131332e30222c226d6163223a22373832424342413230393631222c2276657273696f6e223a22312e322e332e34222c226c6173745f6d73675f6964223a2230222c226c6173745f707573685f6964223a2230222c226170705f6e616d65223a2261706164227d"
    print len(tstr)

    print tstr
    i = 0;
    while i< len(tstr):
        #print tstr[i],tstr[i+1]
        i = i + 2
    print "\n"

    #source = [0x69,0x00,0x30,0x00,0xf3,0x2f,0x63,0x1c,
    #        0xc2,0x39,0xad,0xa1,0x05,0xf0,0x91,0x12]

    #en = [0x69,0,0x30,0,0,0,0,0x10,0x1f,0x2,0,0x1,0,0,0,0]


    ts1 = encrypt_xor(tstr)
    print ts1
    #ts2 = decrypt_xor(ts1,len(ts1))
    #print ts2


    #ts3 = decrypt_xor(ts2,len(ts2))
    #print ts3
    
if __name__ == '__main__':
    test()
    
