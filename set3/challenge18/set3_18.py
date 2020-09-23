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

        

if __name__ == '__main__':
    BLOCK_SIZE = 16
    text = b'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
    key = b'YELLOW SUBMARINE'
    text = base64.b64decode(text)
    nonce = 0 
    final = ctr_mode(text,key,nonce)
    print(final)

    
