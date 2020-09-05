import random 
import string
import sys
from Crypto.Cipher import AES
import base64



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
    """
    takes chunks of data, and pads them according to pkcs#7

    param1: array of bytes (list)

    rtype: arrray of padded bytes (list)
    """
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





def recover_one_more_byte(known:bytes,bsize:int,key:int,len_prefix:bytes)->bytes:
    """ takes known secret text and makes it so that we can find the next secret text by appending it with all possible values 

    param1: -> text known before this iteration (bytes)
    param2: -> block size used in encryption    (int)
    param3: -> key to be encrypted with         (bytes)
    param4: -> len of prefix

    r1: -> known with a new known
    """
    #known = b"Rollin' in "

    #we add padding to the prefix to make it obsulute
    prefix_pad = (16 - (len_prefix % 16)) * b'x' 
    # (p+k+1 === 0 mod (16) i.e we work on last letter )
    padding_len = (-len(known)-1) % bsize
     
    #padding_prefix and padding can be ignored 
    reserved_chunks = len_prefix // 16 + 1

    #the chunk that is required right now (ignoring_prefix)
    target_chunk_number = len(known) // 16 + reserved_chunks
    
    padding_data = prefix_pad + b"A" * padding_len
    cipher = encryption_oracle(padding_data,key)
    chunk_text = chunks(cipher,16)
    
    target_chunk = chunk_text[target_chunk_number]
    comp_text = chunks(target_chunk,1)[15] 
 
    
    letters = ",.?'-abcdefghsoijklmnpqrtuvwyxz\n ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    num_let = []
    for z in letters:
        num_let.append(ord(z))



    for i in num_let:
        test_plain = padding_data + known + bytes([i])
    
        test_cipher = encryption_oracle(test_plain,key)
        test_chunks = chunks(test_cipher,16)
        test_target = test_chunks[target_chunk_number]
        comp_test = chunks(test_target,1)[15]


        if comp_text == comp_test:
            #print(len(known)) 
            #print(i,bytes([i]))
            return (bytes([i]))
    
    












def one_byte_a_time(bsize:int,key:bytes,len_prefix:int)->bytes:
    """ finds out the secret key one byte at a time
    param1:-> block size we require 

    r1: -> secret text
    """
    print("A_byte_at_a_time_attack")

    known_plain_text = b''
    len_of_secret = len(encryption_oracle(b'',key))
    
    for i in range(len_of_secret):
        new_known_byte = recover_one_more_byte(known_plain_text,bsize,key,len_prefix)
        known_plain_text = known_plain_text + new_known_byte
        print(known_plain_text)
    print(known_plain_text)
    return known_plain_text


def find_block_size(key:bytes)->int:
    """finds the block size used in encryption
    param1:bytes
    
    r1: int
    """
    text = b"A"
    for i in range(1,64):
        text= text + b"A"
        cipher = encrypt_aes_ecb(text,key)
        if i == 1:
            initial_len = len(cipher)
        if len(cipher) != initial_len:
            return i

    


def find_repeating_blocks(cip: bytes) -> int:
    """
    find repeated blocks in a chunk text IMP as ecb produces repeated ciphers for same plain text
    """


    chunk_tex = chunks(cip,16)
    repeat = len(chunk_tex) - len(set(chunk_tex))
    return(repeat)


def find_len_prefix(key:bytes,bsize)->int:
    """find the length text that is added to the plain text

    pram1: -> key to encrypt (bytes)
    pram2: -> size of bytes in encryption

    r1: -> length of random prefix
    """
    #find out the upto which chunk the prefix lies

    data_1 = b'A'
    data_2 = b'B'
    ciphers = []
    
    #encrypting two different string of same length. the prefix will give same
    #encryption while plain text wont
    ciph_1 = chunks(encryption_oracle(data_1,key),16)
    ciph_2 = chunks(encryption_oracle(data_2,key),16)

    for k in range(len(ciph_1)):
        if ciph_1[k] != ciph_2[k]:
            #print(k)
            break
    #find the length of prefix in the last chunk it exists 
    for i in range(64):
            #print(i)
            cipher = encryption_oracle(data_1,key)
            #print(cipher[K:K+1616])
            ciphers.append(cipher[k*16:(k*16)+16])
            data_1 = data_1 + b'A'
            if len(ciphers) == 1:
                continue
            if ciphers[i] == ciphers[i-1]:

                return((k+1)*16-i)
        













def encryption_oracle(text:bytes,key:bytes)->bytes:
    """ takes a bunch of text, adds a bunch of additional 
        text, generates a random key and initilization
        vector. then randomly encrypts it in ebc or cbc


    param1: text to be encrypted (bytes)

    rtype: encrypted text (bytes)
    """
    prefix=b'xyeyryryrtru34583rtyuioppoiuhj'
    base64_message = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"  
    message_bytes = base64.b64decode(base64_message)
    front = message_bytes
    
    

    text = prefix + text + front
    
    cipher = encrypt_aes_ecb(text,key)
    #plaintext = decrypt_aes_ecb(cipher,key)
    return(cipher)




if __name__ == '__main__':
    fhandle = open("text.txt","rb")
    text = fhandle.read()
       
    key = b'YELLOW SUBMARINE'

    block_size = find_block_size(key)
    #print(block_size)

    cipher = encryption_oracle(text,key)
    mode = find_repeating_blocks(cipher)
    if mode > 0:
        print("Encryption Used is ECB")

    len_prefix = find_len_prefix(key,16)
    print("length of prefix: ",len_prefix)
    
    secret_text = one_byte_a_time(block_size,key,len_prefix) 

    #for i in range(100):
    #    cipher = encryption_oracle(text,key)
    #    print(cipher)

