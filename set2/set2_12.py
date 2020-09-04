import random 
import string
import sys
from Crypto.Cipher import AES
import base64


def encryption_oracle(text:bytes,key:bytes)->bytes:
    """ takes a bunch of text, adds a bunch of additional 
        text, generates a random key and initilization
        vector. then randomly encrypts it in ebc or cbc


    param1: text to be encrypted (bytes)

    rtype: encrypted text (bytes)
    """

    base64_message = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"  
    message_bytes = base64.b64decode(base64_message)
    front = message_bytes
    
    

    text = text + front
    
    cipher = encrypt_aes_ecb(text,key)
    #plaintext = decrypt_aes_ecb(cipher,key)
    return(cipher)


def recover_one_more_byte(known:bytes,bsize:int,key:int)->bytes:
    """
    """
    #known = b"Rollin' in "
    padding_len = (-len(known)-1) % bsize

    target_chunk_number = len(known) // 16
    
    padding_data = b"A" * padding_len
    cipher = encryption_oracle(padding_data,key)
    chunk_text = chunks(cipher,16)
    
    target_chunk = chunk_text[target_chunk_number]
    comp_text = chunks(target_chunk,1)[15] 
 
 
    letters= b"abcdefghijklmnopqrstuvwxyz :',." 
    for i in range(0,256):
        test_plain = padding_data + known + bytes([i])
    
        test_cipher = encryption_oracle(test_plain,key)
        test_chunks = chunks(test_cipher,16)
        test_target = test_chunks[target_chunk_number]
        comp_test = chunks(test_target,1)[15]


        if comp_text == comp_test:
            if i == 9 or i ==28 or i == 68 or i == 7 or i== 91 or i == 16 or i == 72 or i == 17 or i == 54 or i == 8 or i == 0 or i == 43:
                continue
    
            if len(known) == 31:
                if bytes([i]) == b'n':
                    continue
            if len(known) == 34:
                if bytes([i]) == b'5':
                    continue
            if len(known) == 40 or len(known)==42 or len(known)==43:
                if bytes([i]) == b'E' or bytes([i]) == b")" or bytes([i])==b'5':
                    continue

            

            print(len(known)) 
            #print(i,bytes([i]))
            return (bytes([i]))
    
    












def one_byte_a_time(bsize:int,key:bytes)->bytes:
    """
    param1: block size we require 

    rerturn secret text



    """
    print("A_byte_at_a_time_attack")

    known_plain_text = b''
    len_of_secret = len(encryption_oracle(b'',key))
    
    for i in range(len_of_secret):
        new_known_byte = recover_one_more_byte(known_plain_text,bsize,key)
        known_plain_text = known_plain_text + new_known_byte
        print(known_plain_text)
    print(known_plain_text)
    return known_plain_text


    """
    plain_text = b''


    secret = b''
    for j in range():
        plain_text = b''
        print(j)
        bsize = bsize - 1
        for k in range(bsize):
            plain_text = plain_text + b'A'
        if bsize == 15:
            compare_when_iter = plain_text


        cipher = encryption_oracle(plain_text,key)
        chunk_text = chunks(cipher,16)
        print(chunk_text)
        test = chunk_text[0]
        secret_text = chunks(test,1)[15] 
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
        for i in letters:
                temp = compare_when_iter + bytes(i.encode('utf-8'))

                test_cipher = encryption_oracle(temp,key)
                test_chunks = chunks(test_cipher,16) 
                print(test_chunks)
                test_text =  test_chunks[0]
                com_text = chunks(test_text,1)[15]
    
                if com_text == secret_text:
                    secret = secret + bytes(i.encode('utf-8'))
                    print(temp) 
                    compare_when_iter = str(temp)[3:18].encode('utf-8')
                    print(len(compare_when_iter))
                
    print("This",secret)

"""
def find_block_size(key:bytes):
    text = b"A"
    for i in range(1,64):
        text= text + b"A"
        cipher = encrypt_aes_ecb(text,key)
        if i == 1:
            initial_len = len(cipher)
        if len(cipher) != initial_len:
            return i

    


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


if __name__ == '__main__':
    fhandle = open("text.txt","rb")
    text = fhandle.read()
       
    key = b'YELLOW SUBMARINE'

    block_size = find_block_size(key)
    print(block_size)

    cipher = encryption_oracle(text,key)
    mode = find_repeating_blocks(cipher)
    if mode > 0:
        print("Encryption Used is ECB")

    secret_text = one_byte_a_time(block_size,key) 

    #for i in range(100):
    #    cipher = encryption_oracle(text,key)
    #    print(cipher)

