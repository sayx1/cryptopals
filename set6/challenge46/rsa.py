from get_prime import *
from modinv import *
import Crypto.Util.number

def rsa(msg):
    e = 17
    p = n_Bit_Prime(1024)
    q = n_Bit_Prime(1024)
    n = p*q
    et = (p-1)*(q-1)
    d = modinv(e,et)

    #msg = b'attck at dawn'
    m = Crypto.Util.number.bytes_to_long(msg)
    c = pow(m,e,n)
    #decrypt_msg = pow(c,d,n) 
    #dec = Crypto.Util.number.long_to_bytes(decrypt_msg)
    public = e,n
    private = d,n
    return(c,public)


