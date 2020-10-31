from set4_28 import *
import random

def implement_diffie_hellman():
    n = ("""ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024
e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec
6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f
24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361
c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552
bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff
fffffffffffff""".replace('\n',""))
    
    n  = int(n,base=16)

    
    g = 2
    #// private keys 
    a = random.randint(1,n)
    b = random.randint(1,n)
    
    #// public keys
    A = pow(g,a,n) #modexp(g, a, n):
    B = pow(g,b,n) #modexp(g, b, n):
    
    #// encrypting key
    s1 = pow(B,a,n) #modexp(B, a, n):
    s2 = pow(A,b,n) #modexp(A,b,n)   

    s = s1.to_bytes((s1.bit_length() + 7) // 8, 'big')
    if s1 == s2:
        return(SHA_1(s),a,b)
      



def main():
    key,a,b = implement_diffie_hellman()
    print(key)


if __name__ == "__main__":
   main()

