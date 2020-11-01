from set4_28 import *
from AES_128_CBC import *
import random
from pwn import *
import hashlib

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
    
    
    n = ("""ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024
e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec
6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f
24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361
c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552
bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff
fffffffffffff""".replace('\n',""))
    n  = int(n,base=16)
    
    #g = 1
    #g = n
    g = n-1
    
    a,A = get_private_public_key(g,n)
    
    #Sending Public key
    send_port = 5678
    r = remote('localhost', send_port)
    print("send generator")
    r.sendline(str(g))

    print ("C: Sending Alice's Public key")
    r.sendline(str(A))

    #get Bob's Private key 
    B = int(r.recvline(keepends = False))
    print ("C: received B", B)
    
    #calculate a shared key 
    shared_key = get_shared_key(B,a,n)
    key = hashlib.sha1(str(shared_key).encode()).digest()[:16]
    
    iv = os.urandom(16)
    msg = b'attack_at_dawn'
    
    ctxt = encrypt_128_aes_cbc(msg,key,iv)
    
    # Sending Data to Bob 
    print ("C: Sending encrypted message ")
    print(ctxt)
 
    
    to_send = ctxt + iv
    r.sendline(to_send)
     
    
        
    




if __name__ == "__main__":
   main()

