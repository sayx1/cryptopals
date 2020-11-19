import gensafeprime
from base64 import b64decode
from Crypto.Util.number import inverse,bytes_to_long,long_to_bytes
from gmpy2 import f_div
import math
from hashlib import sha1
import os
import numpy as np

### padding pkcs 1.5
def pad_pkcs(msg,n):
    k = (n.bit_length() + 7) // 8
    padding = os.urandom(k - 3 - len(msg))
    return(b'\x00\x02'+padding+b'\x00'+msg)

### rsa encryption enc and dec 
def gen_keys():
    '''
        generates public and private key for RSA encryption 
            with crypto safe prime numbers (1024 bits)
        returns -> ( public ( e , n ) , private ( d , n )  
    '''
    e = 17
    p = gensafeprime.generate(768)
    q = gensafeprime.generate(768)
    n = p*q
    et = (p-1)*(q-1)
    d = inverse(e,et)
    public = e,n
    private = d,n
    return(public,private)

public,private = gen_keys()
i = 0 

def rsa_enc(msg):
    '''
        encrypts cipher using global rsa public keys 
        returns -> cipher encrypted 
    '''
    e,n = public
    m = bytes_to_long(msg)
    c = pow(m,e,n)
    return(c)

def rsa_dec(cipher):
    '''
        decrypts rsa using global private rsa public keys 
        param1 -> cipher to decrypt
        return -> plain text 
    '''
    d,n = private  
    decrypt_msg = pow(cipher,d,n)
    return(decrypt_msg)



###parity oracle 
def parity_oracle(c):
    '''
        blackbox function will return for 0 for even and one for odd
        param1 -> cipher text
        return -> 1 or 0
    '''
    e,n = public
    test = long_to_bytes(rsa_dec(c))
    rem = ( n.bit_length() +7 ) // 8 
    test = (rem - len(test)) * b'\x00' + test 
    print(test) 
    return (b'\x00\x02' in test[0:2])

###attack
def first_S(B,cipher):
    #for the first s when we don't have interval
    e,n = public
    s = (n+ 3*B - 1 ) // (3*B)
    while True:
        c = (cipher * pow(s,e,n)) % n
        if parity_oracle(c):
            i = 1
            return(s,c)
        s +=1
        

def next_S(M,s,B,cipher):
    e,n = public
    if len(M)>1:
        while True:
            s += 1
            c = (cipher * pow(s,e,n)) % n
            if parity_oracle(c):
                return(s,c)
    else:
        #when we calculate only one interval 
        a,b = M[0]
        r = (2*(b*s - 2*B) + n - 1)//n
        while True:
            low_s = (2*B + r*n + b - 1)//b
            high_s = (3*B + r*n + a - 1)//a 
            for s in range(low_s,high_s):  
                c = (cipher*pow(s,e,n)) % n
                if parity_oracle(c):
                    return(s,c)
            r += 1
    
     
def gen_Next_Interval(M,s,B):
    if len(M) == 0:
        raise Exception('unexpected __||__')
    e,n = public
    Mnew = []
    for a,b in M:
        min_r = (a*s - 3*B + 1 + n - 1 )//n
        max_r = ( b*s - 2*B )//n
        for r in range(min_r,max_r+1):
            next_a = max(a,(2*B + r*n + s - 1 )//s)
            next_b = min(b,(3*B - 1 + r*n )//s)
            if next_a > next_b:
                continue

            Mnew += [(next_a,next_b)]

    if len(Mnew)==0:
        raise Exception('unexpected __\/__') 
    return Mnew

def trim(M,ciphertext):
    e,n = public
    a,b = M[0]
    u_l = []
    t_l = []
    for t in range(pow(2,12)):
        if(t<=50):
            u = (( 2*t + 3-1)//3)
            while(u< (3*t//3) ):
                t_inv = inverse(t,n)
                c = ciphertext*u*t_inv % n
                if(parity_oracle(c)):
                    t_l.append(t)
                    u_l.append(u)
                u += 1
        else:
            u_iter = (t-1//t,t+1//t)
            for u in u_iter:
                t_inv = inverse(t,n)
                c = ciphertext*u*t_inv % n
                if(parity_oracle(c)):
                    t_l.append(t)
                    u_l.append(u)
    t_das = np.lcm.reduce (t_l)
    u_high = max(u_l)
    u_low = min(u_l)
    a = (a * (t_das))//u_low
    b = (b * (t_das))//u_high
    return[(a,b)]


def bleichenbacher_pkcs_1(ciphertext):
    e , n = public
    k = ( n.bit_length() + 7 ) // 8
    B = pow(2,(8*k)-16)
    M = [( 2*B, 3*B-1 )]
    #M = trim(M,ciphertext)
    #M = [(a,b)]
    print(M)
    
    s,c = first_S(B,ciphertext)
    M = gen_Next_Interval(M,s,B)    
    while True:
        if (len(M)==1 and M[0][0]==M[0][1]):
            m = M[0][0]
            m = long_to_bytes(m)
            print(m)
            return(b'\x00'+m)
        print('here')
        s,c = next_S(M,s,B,ciphertext)
        M = gen_Next_Interval(M,s,B)    
    
if __name__ == '__main__':
    e , n = public
    msg = b"kick it, CC"
    padded_msg = pad_pkcs(msg,n)
    c = rsa_enc(padded_msg)
    bleichenbacher_pkcs_1(c) 
    #print(parity_oracle(c))
    
