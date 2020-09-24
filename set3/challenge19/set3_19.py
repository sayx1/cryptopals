import base64
from Crypto.Cipher import AES


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

def ctr_keystream(key:bytes,nonce:int)->bytes:
    counter = 0 
    nonce_bytes = nonce.to_bytes(BLOCK_SIZE //2, byteorder='little')
    while True:
        counter_bytes  = counter.to_bytes(BLOCK_SIZE //2, byteorder='little')
        yield from encrypt_128_aes_ecb(nonce_bytes + counter_bytes ,key)
        counter += 1

def ctr_mode(text:bytes,key:bytes,nonce:int)->bytes:
    if len(text) == 0:
        return b''
    else:
        return(xor_chunks(text,ctr_keystream(key,nonce)))

def encrypted_text()->list:
    nonce = 0 
    key = b'YELLOW SUBMARINE'
    fhandle = open('ctxt','r')
    text = fhandle.read().split('\n')[:-1]
    text = list(map(base64.b64decode,text[:]))
    ciphers = [ctr_mode(i,key,nonce) for i in text]
    return ciphers 



if __name__ == '__main__':
    BLOCK_SIZE = 16
    ciphers = encrypted_text()
    key = b'abcdefghijklmnopqrstuvwxyzabjdsfadskfjasdlkfjdsalakfsdakldsdfklafassdfa'
    
    while True:
        print('enter key index to change')
        location = int(input())
        print('new letter in index')
        key_letter = input()
        key = key[:location] + bytes(key_letter, 'utf-8') + key[location+1:]
        print(key)
        plain_text = [xor_chunks(i,key) for i in ciphers]
        [print(x) for x in plain_text]


