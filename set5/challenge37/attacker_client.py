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
    return salt,I

def main():
    s,I = generate_salt_password()
    x = 0
    
    ##  REGISTRATION
    send_port = 1234
    r = remote('localhost', send_port)
    
    ### Setting Up Connection
    a = 0
    print("C: Sending Username")
    r.sendline(str(I))

    ##getting B
    print("C: Receiving  B")
    B = int(r.recvline(keepends = False))
    print ("C: received B")
    
    ##sending A
    print("C: Sending A")
    A = 0
    r.sendline(str(A))


    ##calculating u
    u = hashlib.sha1(str(A).encode()+str(B).encode()).digest()
    u = Crypto.Util.number.bytes_to_long(u)

    ##calculating shared key 
    Shared_Key_Client = 0 #pow(B - k*pow(g,x,N), a+u*x, N)
    M1 = hashlib.sha256(str(A).encode()+str(B).encode()+str(Shared_Key_Client).encode()).digest().hex()
    print(Shared_Key_Client)
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

