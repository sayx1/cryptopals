import hashlib
import Crypto.Util.number
import random 
from pwn import *
k = 3
g = 2
N = 6277101735386680763835789423207666416083908700390324961279

def generate_salt_password():
    salt = 'YELLOW SUBMARINE'
    I = 'sayx1'
    password ='$up3r_$3cr3t'
    x = hashlib.sha256(salt.encode()+I.encode()+password.encode()).digest()
    x = Crypto.Util.number.bytes_to_long(x)
    v = pow(g,x,N)
    return salt,password,I,v,x
def main():
    s,p,I,v,x = generate_salt_password()
    
    ##  REGISTRATION
    send_port = 1234
    r = remote('localhost', send_port)
    print("C: Sending Username")
    r.sendline(str(I))
    print("C: Sending Salt")
    r.sendline(str(s))
    print("C: Sending verifier")
    r.sendline(str(v))
    

    ### Setting Up Connection
    a = random.randint(1,N)
    print("C: Sending Username")
    r.sendline(str(I))

    ##getting B
    print("C: Receiving  B")
    B = int(r.recvline(keepends = False))
    print ("C: received B")
    
    ##sending A
    print("C: Sending A")
    A = pow(g,a,N)
    r.sendline(str(A))


    ##calculating u
    u = hashlib.sha1(str(A).encode()+str(B).encode()).digest()
    u = Crypto.Util.number.bytes_to_long(u)

    ##calculating shared key 
    Shared_Key_Client = pow(B - k*pow(g,x,N), a+u*x, N)
    M1 = hashlib.sha256(str(A).encode()+str(B).encode()+str(Shared_Key_Client).encode()).digest().hex()

    print("C: Sending M1")
    r.sendline(str(M1))
    
    
    print("C: Receiving  Verification Msg")
    M2 = str(r.recvline(keepends = False).decode())
    print ("C: received M2")

    M2_test =  hashlib.sha256(str(A).encode()+M1.encode()+str(Shared_Key_Client).encode()).digest().hex()
    if (M2 == str(M2_test)):
        print("Verified Established Connection")
    else:
        print("Connection Terminated")

if __name__ == "__main__":
   main()

