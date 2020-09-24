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
    """
    param1: key to encrypt
    param2: nonce to encrypt
    return: returns cipher text 

    the cipher text using generator 
    """
    counter = 0 
    nonce_bytes = nonce.to_bytes(BLOCK_SIZE //2, byteorder='little')
    while True:
        counter_bytes  = counter.to_bytes(BLOCK_SIZE //2, byteorder='little')
        yield from encrypt_128_aes_ecb(nonce_bytes + counter_bytes ,key)
        counter += 1

def ctr_mode(text:bytes,key:bytes,nonce:int)->bytes:
    """
    param1: text to encrypt
    param2: key to encrypt
    param3: nonce to encrypt
    returns xored chunks text and keystream
    """
    if len(text) == 0:
        return b''
    else:
        return(xor_chunks(text,ctr_keystream(key,nonce)))

def encrypted_text()->list:
    '''
    returns the cipher text by encrypting text from ctxt
    '''
    nonce = 0 
    key = b'YELLOW SUBMARINE'
    fhandle = open('ctxt','r')
    text = fhandle.read().split('\n')[:-1]
    text = list(map(base64.b64decode,text[:]))
    ciphers = [ctr_mode(i,key,nonce) for i in text]
    return ciphers 

def freq_score(txt:str)->int:
    """
    who knew this was olny what you need, takes a byte and gives a score 
    based on the bytes in the text
    """
    englishLetterFreq = {'a': .08167, 'e': .12702,  'o': .07507, 't': .09056,
         ' ': .23}
     
    return sum([englishLetterFreq.get(chr(byte), 0) for byte in txt.lower()])

def break_single_key_xor(cipher_txt:bytes):
    x = [xor_chunks(cipher_txt,bytes([i])*len(cipher_txt)) for i in range(256)]
    scores = [freq_score(x[i]) for i in range(256)]

    return bytes([scores.index(max(scores))])

def breaking_repeating_xor(cipher_txt:bytes,key_size:int)->bytes:
    possible_key = b''

    for i in range(key_size):
        block = b''
        for j in range(i,len(cipher_txt),key_size):
            block += bytes([cipher_txt[j]]) 
        possible_key += break_single_key_xor(block)
    return possible_key 


    



if __name__ == '__main__':
    BLOCK_SIZE = 16
    ciphers = encrypted_text()
    key_size = min([len(i) for i in ciphers])
    working_cipher = b''
    working_ciphers = [i[:key_size] for i in ciphers]
    working_cipher = b''.join(working_ciphers)
    xyz = breaking_repeating_xor(working_cipher,key_size)
    for i in ciphers:
        print(xor_chunks(i,xyz))

            
