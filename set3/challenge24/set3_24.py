import base64
from Crypto.Cipher import AES
from set3_21 import *
from time import time
from random import randint

def encrypt_128_aes_ecb(text:bytes,key:bytes)->bytes:
    cipher = AES.new(key,AES.MODE_ECB)
    cipher_text = cipher.encrypt(text)
    return cipher_text

def decrypt_128_aes_ecb(text:bytes,key:bytes)->bytes:
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = cipher.decrypt(text)
    return plaintext


def xor_chunks(text:bytes,p_text:bytes)->bytes:
    return bytes([_a ^ _b for _a, _b in zip(text, p_text)])

def mt19937_keystream_generator(key):
    '''
    generate a keystream with prng
    '''
    prng = MT19937_32(key)
    while True:
        number = next(prng)

        yield from number.to_bytes(4, byteorder='big')


def encrypt_CTR(msg:bytes,key:bytes):
    '''
    generate a keystream with prng
    '''
    keystream = mt19937_keystream_generator(key)
    return xor_chunks(msg,keystream)


def randomkey(length:int)->bytes:
    """
    function returns a random key of given length
    param1: length of key (int)
    
    return: key (bytes)
    """
    letters = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    key = b''
    for i in range(length):
        j = randint(1,62)
        key = key + letters[j:j+1]
    return key

def encryption()->bytes:
    '''adds random text to the known plaintext and encrypts it under 16
       bits generated using current time
    '''
    text = b'AAAA' * 4
    j = (randint(2,19))
    plain = randomkey(j) + text 
    seed = int(time()) & 0xFFFF
    return (encrypt_CTR(plain,seed))

def break_cipher(cipher:bytes):
    '''takes a cipher whoose portion of plain text is known and loops 
    through 16 bit keyspace and decrpts it. if decrypted text has the known 
    plain text we get the text and seed
    '''
    plain = b'AAAA' * 4
    for i in range(2**16):
        cip = encrypt_CTR(cipher,i)
        if plain in cip:
            return(cip,i)


            
if __name__ == '__main__':
    BLOCK_SIZE = 16
    seed = int(time()) & 0xFFFFFFFF
    cipher = encryption()
    plain,seed = break_cipher(cipher)
    print('Plain: ',plain,'& Seed: ',seed)

        
    
          
