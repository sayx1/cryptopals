import gensafeprime
from base64 import b64decode
from Crypto.Util.number import inverse,bytes_to_long,long_to_bytes
from gmpy2 import f_div
import math


def gen_keys():
    e = 17
    p = gensafeprime.generate(1024)
    q = gensafeprime.generate(1024)
    n = p*q
    et = (p-1)*(q-1)
    d = inverse(e,et)
    public = e,n
    private = d,n
    return(public,private)

public,private = gen_keys()

def rsa_enc(msg):
    e,n = public
    m = bytes_to_long(msg)
    c = pow(m,e,n)
    return(c)

def rsa_dec(cipher):
    d,n = private  
    decrypt_msg = pow(cipher,d,n)
    return(decrypt_msg)

def parity_oracle(c):
    plain_text = rsa_dec(c)
    return plain_text % 2

def dec_plaintext(c,secret_msg):
    print(secret_msg)
    e,n = public
    lower_bound = 0
    upper_bound = n
    for i in range(1, int(math.log(n, 2)+1)):
        multiplier = pow(2, i*e, n)
        is_odd = parity_oracle(multiplier*cipher)
        if is_odd:
            lower_bound = int(f_div(upper_bound+lower_bound,2).digits())
        else:
            upper_bound = int(f_div((upper_bound+lower_bound),2).digits())
        
        if i%10 == 0:
            print ('upper_bound', long_to_bytes(upper_bound))

        if secret_msg in long_to_bytes(upper_bound):
            break
    return(upper_bound)



if __name__ == '__main__':
    msg = 'VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=='
    msg = b64decode(msg)
    cipher = rsa_enc(msg)
    plain_text = dec_plaintext(cipher,msg)
    print(plain_text)


    
