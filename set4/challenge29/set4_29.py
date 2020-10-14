import hashlib
from set4_28 import *
from binascii import b2a_hex
import random
import os

def chunks(text:bytes,blocksize:int)->bytes:
    """
            pram1: whole encrypted messages 
            pram2: amount of chunks needed 

            return array of chunks of data
    """
    chunk_data = b''
    chunks = []
    for i in range(0,len(text),blocksize):
        chunk_data = text[i:i+blocksize] 
        chunks.append(chunk_data)
    return chunks



def get_internal_states(msg_digest:bytes)->list:
    a = msg_digest >> 128
    b = (msg_digest >> 96) & 0xffffffff
    c = (msg_digest >> 64) & 0xffffffff
    d = (msg_digest >> 32) & 0xffffffff
    e = msg_digest & 0xffffffff
    
    return ((a,b,c,d,e))

def validate(msg,digest):
    '''meant to act like a server which takes msg and digest and verifies the 
        MAC
    '''
    key = b'YELLOW SUBMARINE'
    actual_digest = SHA_1(key+msg)
    if digest == actual_digest:
        return 1
    else: 
        return 0 

def server(msg:bytes):
    ''' meant to imitate the server which takes a msg and gives you the MAC
    '''
    key = b'YELLOW SUBMARINE'
    return(SHA_1(key+msg))

def sha1_padding(msg, forced_msg_byte_length=None):
    ''' implements sha_1 padding for message with optional parameter for
        SHA-1 keyed MAC using length extension
        taken from custom implementation
    '''

    if forced_msg_byte_length == None:
        ml = len(msg)*8
    else:
        ml = forced_msg_byte_length*8
    
    m = -(ml + 1 + 64) % 512
    padded_msg = msg + bytes([0b10000000]) + b'\x00'*(m//8) + ml.to_bytes(8, byteorder='big')
                 
    return padded_msg



def guess_key_len(msg,digest):
    ''' takes the msg and digest, guesses the key len and gives a 
            digest in line with the mac
    '''
    digest = int(b2a_hex(digest),16)
    states = get_internal_states(digest)
    print('[+] Initilizing Key Guesses')
    for keylen in range(512):
        key = b'A'* keylen
        padding = sha1_padding(key+msg)[keylen+len(msg):]
        injection = b';admin=true;'
        forged_msg_len = keylen + len(msg) + len(padding) + len(injection)
        test_digest = SHA_1(injection,states[0],states[1],states[2],states[3],states[4],forged_msg_len)
        forged_msg = msg + padding + injection
        print('[+] Validating Keylen = ',keylen)
        if validate(forged_msg,test_digest):
           print('[+]Sucessfully Generated MAC with Keylen ',keylen,'MAC is :') 
           print(test_digest)
           return(test_digest)


def main():
    message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"

    
    digest = server(message)
    key_len = guess_key_len(message,digest)





if __name__ == '__main__':
        main()

