from set4_28 import *
from AES_128_CBC import *
import random
from pwn import *

def get_private_public_key(g,n):
    #   //privatekeys
    a = random.randint(1,n)
        
    #   // public keys
    A = pow(g,a,n) #modexp(g, a, n):
    return(a,A)
              
def get_shared_key(A,a,n):
    return(pow(A,a,n))


def main():
    #generators
    g = 2
    n = ("""ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024
e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec
6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f
24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361
c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552
bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff
fffffffffffff""".replace('\n',""))
    n  = int(n,base=16)
    
    b,B = get_private_public_key(g,n)
    
    #Receiving Public key
    s = listen(1234)
    A = int(s.recvline(keepends = False))
    
    #Sending Bob's Public key
    s.sendline(str(B))

    #calculate a shared key 
    shared_key = get_shared_key(A,b,n)
    key = hashlib.sha1(str(shared_key).encode()).digest()[:16]
    

    #Receive the encrypted msg
    ctext = s.recvline(keepends = False)
    print ("S: Received encrypted message ")
    
    ctxt = ctext[:-16]
    iv = ctext[-16:]


    msg = decrypt_128_aes_cbc(ctxt,key,iv)
    
    # Sending Data to Bob 
    print ("C: Printing message ")
    print(msg)
     
    
        
    




if __name__ == "__main__":
   main()

