#-*- coding: utf-8 -*-
import random

def create_token():
    token = ''
    for i in range(64):
        int_10 = random.randint(0,15)
        int_16 = hex(int_10)
        str_16 = int_16[2:]
        token += str_16
        
    return token
    
if __name__ == '__main__':
    token = create_token()
    print token