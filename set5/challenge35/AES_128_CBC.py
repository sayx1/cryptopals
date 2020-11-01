import random 
import string
import sys
from Crypto.Cipher import AES

def encryption_oracle(text:bytes)->bytes:
    """ takes a bunch of text, adds a bunch of additional 
        text, generates a random key and initilization
        vector. then randomly encrypts it in ebc or cbc


    param1: text to be encrypted (bytes)

    rtype: encrypted text (bytes)
    """

    text = additional_text(text) 
    for i in range(100):
        key = randomkey(16)
        #print(key)
        iv =  randomkey(16)
        #print(len(iv))
        if len(key)==16 and len(iv) == 16:
            break

    n = random.randint(0,1)
    print("n=",n)
    

    if n == 1 :
        cipher = encrypt_128_aes_cbc(text,key,iv)
        #plaintext = decrypt_128_aes_cbc(cipher,key,iv)
        return(cipher)
    
    elif n == 0:
        cipher = encrypt_aes_ecb(text,key)
        #plaintext = decrypt_aes_ecb(cipher,key)
        return(cipher)



def find_repeating_blocks(cip: bytes) -> int:


    chunk_tex = chunks(cip,16)
    repeat = len(chunk_tex) - len(set(chunk_tex))
    #for i in range(len(chunk_tex)):
    #    for j in range(i+1,len(chunk_tex)):
    #        if chunk_tex[i] == chunk_tex[j]:
    #    
    #            repeat = repeat + 1

    return(repeat)




def encrypt_aes_ecb(text:bytes,key:bytes)->bytes:
    """ takes a bunch of text and splits it in chunks, pads it in 
        pkcs (#PKCS7)
    param1 : text to be encrypted (bytes)
    key : key to encrypt (bytes)

    r_type : cipher text (bytes)

    """

    chunk_text = chunks(text,16)
    padded_chunks = padded_text(chunk_text)
    cipher_text = b''
    for i in padded_chunks:
    
        cipher = encrypt_128_aes_ecb(i,key)
        cipher_text += cipher
    return cipher_text 



def decrypt_aes_ecb(cipher_text:bytes,key:bytes)->bytes:
    """ takes a bunch of cipher text and splits it in chunks and
        returns plain text
    param1 : text to be encrypted (bytes)
    key : key to encrypt (bytes)

    r_type : cipher text (bytes)

    """

    chunk_text = chunks(cipher_text,16)
    plain_text = b''
    for i in chunk_text:
        '''
        print("i",i)
        print("previous",previous_chunk)
        print("")
        '''
        plain = decrypt_128_aes_ecb(i,key)
        plain_text = plain_text + plain
    return plain_text


         

def encrypt_128_aes_cbc(text:bytes,key:bytes,iv:bytes)->bytes:
    """function to take plaintext and encrypt it using aes 128 cbc 

    param1 -> plaintext
    param2 -> key to encrypt data
    iv -> initilization vector

    return cipher text 

    """
    chunk_text = chunks(text,16)
    padded_chunks = padded_text(chunk_text)
    previous_chunk = iv
    cipher_text = b''
    for i in padded_chunks:
        xor_text = xor_chunks(i,previous_chunk)
        cipher = encrypt_128_aes_ecb(xor_text,key)
        previous_chunk = cipher
        cipher_text += cipher
    return cipher_text



def decrypt_128_aes_cbc(cipher_text,key,iv):
    chunk_text = chunks(cipher_text,16)
    previous_chunk = iv
    plain_text = b''
    for i in chunk_text:
        '''
        print("i",i)
        print("previous",previous_chunk)
        print("")
        '''
        plain = decrypt_128_aes_ecb(i,key)
        xor_text = xor_chunks(plain,previous_chunk)
        plain_text = plain_text + xor_text
        previous_chunk = i
    return plain_text




        
   
def padding(msg:bytes, bsize:int)->bytes:
    """ pad the message to the blocksize using the PKCS#7 padding scheme 
    :param msg -> message to pad (bytes)
    :param bsize -> the block size to use (int)

    return padded message (bytes)
    """

    if bsize<2 and bsize>255:
        raise ValueError

    msg_len = len(msg)
    pad_size = bsize - (msg_len % bsize)
    pad_val = pad_size.to_bytes(1, sys.byteorder, signed=False)
    padding = pad_val * pad_size
    return(msg+padding)





def randomkey(length:int)->bytes:
    """
    function returns a random key of given length
    param1: length of key (int)
    
    return: key (bytes)
    """
    letters = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    key = b''
    for i in range(length):
        j = random.randint(1,62)
        key = key + letters[j:j+1]
    return key





def additional_text(text:bytes)->bytes:
    """appends a random number of letter to the front and back of the plain text
    pram1 -> plain text data

    rturn plain text with random letters front and back
    """
    frontlen = random.randint(5,10)
    backlen = random.randint(5,10)
    front = randomkey(frontlen)
    back = randomkey(backlen)
    return (front + text + back)






def padded_text(chunk_text:bytes)->bytes:
    
    padded_chunks = []
    for i in chunk_text:
        if len(i) != 16:
            padded_chunks.append(padding(i,16))
        else:
            padded_chunks.append(i)

    return padded_chunks



def xor_chunks(text:bytes,p_text:bytes)->bytes:
    return bytes([_a ^ _b for _a, _b in zip(text, p_text)])





def encrypt_128_aes_ecb(text:bytes,key:bytes)->bytes:
    cipher = AES.new(key,AES.MODE_ECB)
    cipher_text = cipher.encrypt(text)
    return cipher_text



def decrypt_128_aes_ecb(text:bytes,key:bytes)->bytes:
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = cipher.decrypt(text)
    return plaintext



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
