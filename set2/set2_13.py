import random 
import random 
import string
import sys
from Crypto.Cipher import AES




def k_v_prase(data:bytes)->dict:
    """
    takes a string in form of email=xas@gmail.com&uid=10&role=admin 
    and returns a dictornary in the form of {'email': 'xas@gmail.com', 'uid': '10', 'role': 'admin'}

    param1: data (bytes)

    return: data (dict)
    """
    data = data.split("&")
    r_data = {}
    for i in data:
        i = i.split("=")
        r_data[i[0]] = i[1]
    return(r_data)




def profile_maker(data:bytes)->dict:
    """
    takes in email address changes it in format of data = email=email&uid=10&role=user
    encrypts it under a consistent key and returns the key and encrypted data

    param1: suresh@gmail.com (bytes)
    
    rtype: {cipher (bytes),key (bytes)} 
    """

    for email in data:
        if email == "&" or ord(email) == 38 or email == '=' or ord(email) == 61:
            return('nicetryson')
    

    #uid = random.randint(10,19)
    role = 'user'
    to_send = 'email'+'='+data+'&'+'uid'+'='+str(10)+'&'+'role'+'='+role
    #print(to_send)
    key = b'YELLOW SUBMARINE'
    """
    for i in range(100):
        key = randomkey(16)
        if len(key) == 16:
            break
    """
    encoded_profile = cipher = encrypt_aes_ecb(to_send.encode('utf-8'),key)
    return(encoded_profile,key)
    #return(k_v_prase(to_send))









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

def unpad_pkcs7(buffer):
    padding = buffer[-1]
    for i in range(len(buffer) - 1, len(buffer) - padding - 1, -1):
        if buffer[i] != buffer[-1]:
            return buffer
    new_buffer = bytearray()
    new_buffer[:] = buffer[:-padding]
    return new_buffer

def decrypt_profile(data:dict):
    """
    takes dict with (cipher-of-profile_data,key)
    and gives out data in format of {'email': 'xas@gmail.com', 'uid': '10', 'role': 'admin'}

    :param1 -> dictonary with {cipher(bytes),key(bytes)}
    

    """
    profile = data[0]
    key = data[1]
    profile_decoded = unpad_pkcs7(decrypt_aes_ecb(profile,key)).decode('utf-8')
    print(profile_decoded)
    print(k_v_prase(profile_decoded))






def cut_paste_ecb():
    """ generates a profile with admin privilages using cut paste ecb
        based on the fact that under same key with same data aes ecb gives same         cipher text

        so first we take a mail and ensure that second chunk has only admin with        padding that can be used later

        second we take a mail with length such that the last all but last chunks        have 'email=xas@gmail.com&uid=10&role='
    """
    last_part_mail = 'me@her.com'
    val = 11
    pad_val = val.to_bytes(1, sys.byteorder, signed=False) * val
    text = last_part_mail + 'admin' + pad_val.decode('utf-8')
    data_2 = profile_maker(text)
    cipher_2 = data_2[0][16:32]
    print(cipher_2)
    
    first_part_mail = 'xas@gmail.com'
    data_1 = profile_maker(first_part_mail)
    print(len(cipher_2))
    cipher_1 = data_1[0][0:32]
    
    final = []
    final = [cipher_1 + cipher_2,data_2[1]]
    decrypt_profile(final)


                
if __name__ == '__main__':
    cut_paste_ecb()


""""

data = profile_maker('sureshpantha40@gmail')
if data == 'nicetryson':
    print('nicetryson')
else:
    cut_paste_ecb()
   #decrypt_profile(data)
"""
