import Crypto.Util.number
import gensafeprime
import gmpy

def generate_keys():
    e = 3
    p = gensafeprime.generate(1024)
    q = gensafeprime.generate(1024)
    n = p*q
    et = (p-1)*(q-1)
    d = Crypto.Util.number.inverse(e,et)
    return(d,e,n)

def rsa(msg):
    d,e,n = generate_keys()
    m = Crypto.Util.number.bytes_to_long(msg)
    
    c = pow(m,e,n)
    decrypt_msg = pow(c,d,n) 
    dec = Crypto.Util.number.long_to_bytes(decrypt_msg)
    print(dec)
    return(c,n)


