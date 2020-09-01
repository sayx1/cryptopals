import base64
from Crypto.Cipher import AES
import binascii
import string

def bytes_to_str(byte_list):
    return "".join(filter(lambda x: x in string.printable, "".join(map(chr, byte_list))))


def decrypt_128_aes_ecb(text,key):
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = cipher.decrypt(bytes(text))
    return plaintext

def encrypt_128_aes_ecb(text,key):
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = cipher.encrypt(text)
    return plaintext 

def pkcs_padding(cipher,blocksize):
    padding_len = blocksize - len(cipher)
    for i in range(padding_len):
        cipher = cipher + bytes([padding_len])
    return(cipher)

def chunks(text,blocksize):
    chunks = []
    for i in range(0,len(text),blocksize):
        chunks.append(bytes(text[i:i+blocksize]))
    return chunks

def xor_chunks (text,iv):
    ans = bytearray([_a ^ _b for _a, _b in zip(bytearray(text),bytearray(iv))])
    return ans
    
 
def encrypt_128_aes_cbc(text,key,iv):
    chunk_text = chunks(text,16)
    padded_text = [pkcs_padding(i,16) for i in chunk_text]
    previous_chunk = iv
    cipher_text = []
    for i in padded_text:
        xor_text = xor_chunks(i,previous_chunk)
        cipher = encrypt_128_aes_ecb(xor_text,key)
        cipher_text.append(cipher)
        previous_chunk = cipher  

    return cipher_text


def decrypt_128_aes_cbc(text,key,iv):
    chunk_text = chunks(text,16)
    print(chunk_text)
        #padded_text = [pkcs_padding(i,16) for i in chunk_text] 
    previous_chunk = iv
    plain_text = []
    for i in chunk_text:  
        decrypted = decrypt_128_aes_ecb(i,key)
        plain_text.append(xor_chunks(decrypted,previous_chunk))
       
        previous_chunk = i

    return plain_text

   # '''




byte_string = b''
fhandle = open('data.txt').readlines()
for line in fhandle:
    line = binascii.a2b_base64(line.strip())
    byte_string += line 
key = b'YELLOW SUBMARINE'
iv =  b'\x00'*16






key = b'YELLOW SUBMARINE'
iv =  b'newtexthoyotakva'

#cipher = encrypt_128_aes_cbc(text,key,iv)
plain = decrypt_128_aes_cbc(byte_string,key,iv)
#print(cipher)
for i in plain: 
    print(i)

