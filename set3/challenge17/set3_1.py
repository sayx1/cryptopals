import random
import base64
from Crypto.Cipher import AES
import sys
import os 
import itertools


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
    #print(padding)
    #print(msg)
    return(msg+padding)

def padded_text(chunk_text:bytes)->bytes:
    """ returns padded chunks when chunks are sent using `function`

    param1: list of cipher chunks
    
    return: list of padded text

    """
    
    padded_chunks = []
    for i in chunk_text:
        if len(i) != 16:
            padded_chunks.append(padding(i,16))
        else:
            padded_chunks.append(i)

    return padded_chunks

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
    '''
    param1: cipher to decrypt
    param2: key to decrypt
    iv: initilization vector
    
    this function takes a cipher,key,iv and and it 
    unpads the text if the pcks padding is not vaild 
    then return PaddingError
    '''
    chunk_text = chunks(cipher_text,16)
    previous_chunk = iv
    plain_text = b''
    for i in chunk_text:
        plain = decrypt_128_aes_ecb(i,key)
        xor_text = xor_chunks(plain,previous_chunk)
        plain_text = plain_text + xor_text
        previous_chunk = i
    
    unpaded_text = padding_validation(plain_text)
    return unpaded_text





def unpad_valid_pkcs7(buff):
        '''
        param1: takes a buffer of text
        return: returns unpadded plain text
        if padding is not vaild then it returns Padding Error
        TO WORK THIS DOESN"T WORK FOR UNPADED TEXT
        '''
        if len(buff) % 16 != 0:
            return('PaddingError')
        last_byte = buff[-1]
        if last_byte > 16:
            return("PaddingError")
        for i in range(last_byte, 0, -1):
            if buff[-i] != last_byte:
                return("PaddingError")
        return buff[:-last_byte]
   


def padding_validation(buff:bytes)->list:
    '''
    param1: plain text
    return: unpaded text or Padding Error
    takes plain text buffer and returns unpadded text 
    or PaddingError
    '''
    unpaded_text = unpad_valid_pkcs7(buff)
    return(unpaded_text)



def server(ctxt:bytes):
    '''
    param1: takes buffer of cipher text for decryption 
    return: padding error or done 
    imitates web server 
    '''
    plain = decrypt_128_aes_cbc(ctxt,key,iv)
    if plain == 'PaddingError':
        return('PaddingError')
    else:
        return('done')



def encryptor():
    '''
    return: cipher text 
    takes plain text in file and encrypts it to give key 
    and iv 
    '''
    fhandle = open('set3_1_ctxt')
    text = fhandle.read()
    text = text.split('\n')

    messages = list(map(base64.b64decode,text[:-1]))
    #msg = messages[1]
    msg = random.choice(messages)
   
    while len(msg) % 16 == 0:
        msg = random.choice(messages)
    print(msg)
    ctxt = encrypt_128_aes_cbc(msg,key,iv)
    return(ctxt)



def cbc_padding_attack(ctxt:bytes):
    '''
    param1: cipher using cbc
    takes  a cipher and uses cbc padding attack to 
    get the cipher

    this solution assumes we have no acess to iv 
    and a common one is not used 

    '''

    cipher_chunks = chunks(ctxt,16)
    #the number of iterations for all chunks excluding the first one
    req_times = len(cipher_chunks) // 2 + 1

    final = []  
    #(c0,c1) to (c1,c2) to (c2,c3) ..........
    for i in range(req_times):
        pl = []
        last = []
        num = []
        dec = []
        last_dec = []
        #this goes throuh the sets we will use
        j,k = i,i+1
        c_0 = cipher_chunks[i]
    
        c_1 = cipher_chunks[i+1]
        
        #goes through last byte to first getting plain text 
        #using generated padding
        for l in range(15,0,-1):
    
            paxadi = b''
            #makes the last copule of bytes needed padding
            for a in dec:
                x =  xor_chunks(bytes(a),bytes([16-l]))
                paxadi = paxadi + x
            
            target = c_0
            #goes through all unicode until we get required padding
            for m in range(256):
                #crafted target ciphers 
                target = c_0[:l] + bytes([m]) + paxadi[::-1]
                #tesing our cipher text
                res = server(target+c_1)
                #when we get correct padding
                if res != 'PaddingError':
                    print('found',l)
                    #careful for first byte as '\x00' or '\x01' so we are bound to 
                    #get errors

                    working = xor_chunks(bytes([16-l]),xor_chunks(bytes([m]),c_0[l:l+1]))
                    dec.append(xor_chunks(bytes([16-l]),bytes([m])))
                    pl.append(working)
                    
                    break
        final.extend(pl[::-1]) 
    return(b''.join(final))




if __name__ == '__main__':
    for i in range(100):
        key = randomkey(16)
        #print(key)
        iv =  randomkey(16)
        #print(len(iv))
        if len(key)==16 and len(iv) == 16:
            break
    cipher = encryptor()
    plain_text = cbc_padding_attack(cipher)
    print(plain_text)
    #res = server(cipher)

   
