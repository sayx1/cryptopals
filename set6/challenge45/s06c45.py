import random
import hashlib
from Crypto.Util.number import inverse,bytes_to_long

def poor_sign(msg,pub,priv):
    p,q,g,y = pub
    x = priv
    k = random.randint(1,q-1)
    r = pow(g, k, p) % q

    hash = bytes_to_long(hashlib.sha1(msg).digest())
    
    k_inv = inverse(k,q)
    s = (k_inv * (hash + x * r)) % q
    return(r,s)

def poor_verify(msg,sig,pub):
    hash = bytes_to_long(hashlib.sha1(msg).digest())
    r,s = sig
    p,q,g,y = pub
    w = inverse(s,q)
    

    u1 = (hash * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    print("v: ",v,"r: ",r) 
    return v == r
    

def genKeys(p, q, g):
    x = random.randint(1, q-1)
    y = pow(g, x, p)
    pub = (p, q, g, y)
    priv = x
    return (pub, priv)



if __name__ == '__main__':
    (p, q, g) = (0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1,
                    0xf4f47f05794b256174bba6e9b396a7707e563c5b,
                        0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291)

    
    #generator is 0
    pub,priv = genKeys(p,q,0)
    msg_1 = b'Hello, world'
    sig_1 = poor_sign(msg_1,pub,priv)
    msg_2 = b'Goodbye, world'
    sig_2 = poor_sign(msg_1,pub,priv)
    print("Random Crafted Signature for g==0")
    print("Msg 1 && Signature 2",poor_verify(msg_1,sig_2,pub))
    print("Msg 2 && Signature 1",poor_verify(msg_2,sig_1,pub))

    #generator is p+1
    pub,priv = genKeys(p,q,p+1)
    

    signature = (1, 4325)
    
    print("Random Crafted Signature for g==p+1")
    print("Msg 1 && Signature 2",poor_verify(msg_1,signature,pub))
    print("Msg 2 && Signature 1",poor_verify(msg_2,signature,pub))


