import hashlib
from Crypto.Util.number import bytes_to_long,inverse
import gensafeprime

'''

def generate_keys():
    while(True):
        p = gensafeprime.generate(1024)
        q = gensafeprime.generate(160)
        if((p-1)%q == 0):
            alph = gen_alpha(p,q)
            d = random.randint(1,q-1)
            B = pow(alph,d,p)
            pub = (p,q,alph,B) 
'''

def gen_alpha(p,q):
    alpha = pow(2,(p-1)//q,p)
    if ( pow(alpha,q,p) == 1 ):
        return(alpha)
    else:
        raise Exception('alpha error')

        

def sign_with_k(hash,pub,priv,k):
    (p,q,g,y) = pub
    x = priv
    r = pow(g,k,p) % q
    if r==0:
        return None
    k_inv = inverse(k,q)
    s = (k_inv * (hash + x*r)) % q
    if s == 0:
        return None
    return(r,s)


def verify_signature(message,signature,pub):
    hash = bytes_to_long(hashlib.sha1(message).digest())
    (r,s) = signature
    (p,q,g,y) = pub

    if r <= 0 or r >= q or s <=0 or s>=q:
        return False
    
    w = inverse(s,q)
    u1 = (hash * w) % q
    u2 = (r * w) % q
    v = (( pow(g,u1,p)*pow(y,u2,p) ) % p) % q
    return v == r

def extract_keys(hash,r,s,k,pub):
    (p,q,g,y) = pub
    r_inverse = inverse(r,q)
    return (r_inverse* (s*k-hash)) % q

def are_vaild_keys(pub,priv):
    (p,q,g,v) = pub
    x = priv
    return y == pow(g,x,p)


def brute_force_keys(hash,r,s,pub,kMin,kMax):
    for k in range(kMin,kMax):
        priv = extract_keys(hash,r,s,k,pub)
        if are_vaild_keys(pub,priv):
            return(k,priv)
    return None




if __name__ == '__main__':
        (p, q, g) = (0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1,
                0xf4f47f05794b256174bba6e9b396a7707e563c5b,
                0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291)
        message = b'''For those that envy a MC it can be hazardous to your health
So be friendly, a matter of life and death, just like a etch-a-sketch
''' 
        hash = bytes_to_long(hashlib.sha1(message).digest())
        excepted_hash = 0xd2d0714f014a9784047eaeccf956520045c45265
       
        print(hash)
        if hash != excepted_hash:
            raise Exception(hash + ' != ' + excepted_hash)

        y = 0x84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17
        r = 548099063082341131477253921760299949438196259240
        s = 857042759984254168557880549501802188789837994940
        pub = (p,q,g,y)
        print(verify_signature(message,(r,s),pub))

        k,priv = brute_force_keys(hash,r,s,pub,0,2**16)
        
        expected_hash = 0x0954edd5e0afe5542a4adf012611a91912a3ec16

        if priv == expected_hash:
            raise Exception("private hash doesn't match")

        ( r2, s2) = sign_with_k(hash,pub,priv,k)
        if (r!=r2 or s!=s2):
            raise Exception("k and private key is wrong")
        
        print("k: ",k," ","priv: ",priv)
