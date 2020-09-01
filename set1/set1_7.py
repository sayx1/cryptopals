import base64
from Crypto.Cipher import AES


#opening file to read 

def decrypt_ecb_cipher(text,key):
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = cipher.dfecrypt(text)
    return plaintext

def main():
    key = b'YELLOW SUBMARINE'
    fhandle = open('data.txt')
    text = fhandle.read()
    text = base64.b64decode(text)
    
    message = decrypt_ecb_cipher(text,key)
    print(message)

if __name__ == '__main__':
    main()
