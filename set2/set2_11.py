import base64
from Crypto.Cipher import AES
import binascii
import string
import random
from binascii import a2b_hex


def randomkey(length):
    stringLength= length
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength)).encode()

def addtotext(text):
    frontlen = random.randint(5,10)
    backlen = random.randint(5,10)
    letters = string.ascii_lowercase
    front = ''
    back = ''
    for i in range(frontlen):
        front += random.choice(letters)
    for i in range(backlen):
        back += random.choice(letters)
    return (front + text + back)
    

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
    #padded_text = [pkcs_padding(i,16) for i in chunk_text]
    previous_chunk = iv
    plain_text = []
    for i in text:  
        decrypted = decrypt_128_aes_ecb(i,key)
        plain_text.append(xor_chunks(decrypted,previous_chunk))
       
        previous_chunk = i

    return plain_text

def aes_encrypt(text,key):
    chunk_text = chunks(text,16)
    padded_text = [pkcs_padding(i,16) for i in chunk_text]
    cipher = []
    for i in padded_text: 
        if (len(i)==16):
         encrypted = encrypt_128_aes_ecb(i,key)
         cipher.append(encrypted)
    return cipher

def aes_decrypt(text,key):
    #chunk_text = chunks(text,16)
    #padded_text = [pkcs_padding(i,16) for i in chunk_text]
    cipher = []
    for i in text: 
        if (len(i)==16):
         encrypted = decrypt_128_aes_ecb(i,key)
         cipher.append(encrypted)
    return cipher

def encryption_oracle(text):
    text = addtotext(text) 
    key = randomkey(16)
    #print(key)
    iv =  randomkey(16)
    #print(iv)

    #n = random.randint(0,1)
    n = 1 

    if n:
        cipher = encrypt_128_aes_cbc(text,key,iv)
        #plain = decrypt_128_aes_cbc(cipher,key,iv)
        #print(cipher)
        #print(plain)
        f_cipher = b''
        for i in cipher:
             f_cipher += i
        return(f_cipher)
           
    else:
        cipher = aes_encrypt(text,key)
        #plain = aes_decrypt(cipher,key)
        #print(plain)
        f_cipher = b''
        for i in cipher:
             f_cipher += i
        return(f_cipher)


def detect_ebc(text):
    bin_str = map(bin,bytearray(text))
    repeat = len(bin_str)-len(set(bin_str))
    return(repeat)

   




text = b"orem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
for i in range(100):
    cipher = encryption_oracle(text)
    repeat = detect_ebc(cipher)
    print(repeat)
