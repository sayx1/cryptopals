'''
with help from https://github.com/akalin/cryptopals-python3/blob/master/challenge44.py
'''
from itertools import combinations
from Crypto.Util.number import inverse
import re




def common_k(pub,msg_1,msg_2):
    p,q,g,y = pub
    msg1 , s1 ,r1 ,m1 = msg_1
    msg2 , s2 ,r2 ,m2 = msg_2
    
    ds = s1-s2 % q
    dm = m1-m2 % q
    ds_inv = inverse(ds,q)

    k = (dm * ds_inv) % q
    
    priv_1 = extract_keys(m1,r1,s1,k,pub)
    priv_2 = extract_keys(m2,r2,s2,k,pub)
    if priv_1 == priv_2:
        if are_vaild_keys(pub,priv_1) and are_vaild_keys(pub,priv_2):
            return (k, priv_1)
    return (None, None)



def extract_keys(hash,r,s,k,pub):
    (p,q,g,y) = pub
    r_inverse = inverse(r,q)
    return (r_inverse* (s*k-hash)) % q

def are_vaild_keys(pub,priv):
    (p,q,g,y) = pub
    x = priv
    return y == pow(g,x,p)


def get_priv(text,pub):
    for two_msg in combinations(text,2):
        msg_1,msg_2 = two_msg
        k,priv = common_k(pub,msg_1,msg_2)
        if k:
            return(k,priv)
    return(None,None)

def get_msg():
    text = open('dsa_signed_msg').read().split('\n')[:-1]
    text = [text[i:i+4] for i in range(0,len(text),4)]
    text = new = [(str(msg.split(': ')[-1]),int(r.split(': ')[-1]),int(s.split(': ')[-1]),int(m.split(': ')[-1],16)) for msg,r,s,m in text]
    return(text)

if __name__ == '__main__':
    (p, q, g) = (0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1, 0xf4f47f05794b256174bba6e9b396a7707e563c5b, 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291)
    y = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821
    pub = (p,q,g,y)
    text = get_msg()
    k,priv = get_priv(text,pub)
    print(k,priv)
