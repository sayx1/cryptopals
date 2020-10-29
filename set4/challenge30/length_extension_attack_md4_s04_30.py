from implement_md4 import *
import codecs
import struct
from binascii import b2a_hex



def get_internal_states(msg_digest:bytes):
    states = struct.unpack("<4I", msg_digest)
    return(list(states))


def sha1_padding(msg, msg_len=None):
    ''' implements sha_1 padding for message with optional parameter for
        SHA-1 keyed MAC using length extension
        taken from custom implementation
    '''
    if msg_len is None:
            ml = len(msg) * 8
    else:
            ml = msg_len * 8
    msg += b"\x80"
    msg += b"\x00" * (-(len(msg) + 8) % 64)
    msg += struct.pack("<Q", ml)
    pad = msg 
                 
    return pad


def server(msg:bytes):
    ''' meant to imitate the server which takes a msg and gives you the MAC
    '''
    key = b'YELLOW SUBMARINE'
    digest = MD4(key+msg).hexdigest()
    return(digest)

def encrypt_md4(msg,states=None,length=None):
    digestt = MD4(msg,states,length).hexdigest()
    return(digestt)

def validate(msg,digest):
    key = b'YELLOW SUBMARINE'
    actual_digest = MD4(key+msg).hexdigest()
    print(actual_digest)
    if digest == actual_digest:
        return 1
    else: 
        return 0 


def guess_key_len(msg,digest):
    ''' takes the msg and digest, guesses the key len and gives a 
            digest in line with the mac
    '''
    
    digest = bytearray.fromhex(digest)
    states = get_internal_states(digest)
    
    print('[+] Initilizing Key Guesses')
    for keylen in range(128):
        key = b'A'* keylen
        padding = sha1_padding(key+msg)[keylen+len(msg):]
        injection = b';admin=true;'
        forged_msg_len = keylen + len(msg) + len(padding) + len(injection)
        test_digest = encrypt_md4(injection,states,forged_msg_len)
        print(test_digest)
        forged_msg = msg + padding + injection
        print('[+] Validating Keylen = ',keylen)
        if validate(forged_msg,test_digest):
           print('[+]Sucessfully Generated MAC with Keylen ',keylen,'MAC is :') 
           print(test_digest)
           return(test_digest)
    



if __name__=="__main__":
    message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    digest = server(message)
    guess_key_len(message,digest)

