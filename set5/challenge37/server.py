import hashlib
import Crypto.Util.number
import random
from pwn import *
k = 3
g = 2
N = 6277101735386680763835789423207666416083908700390324961279
users = {}

def create_users(username):
    salt = 'YELLOW SUBMARINE'
    I = 'sayx1'
    password ='$up3r_$3cr3t'
    x = hashlib.sha256(salt.encode()+I.encode()+password.encode()).digest()
    x = Crypto.Util.number.bytes_to_long(x)
    v = pow(g,x,N)
    users[username] = [salt,v]
    


def main():
    #Receiving Public key
    create_users('sayx1')
    server = listen(1234)
    
    #Communication 
    username =  str(server.recvline(keepends = False).decode())
    s,v = users[username]

    # Sending B
    b = random.randint(1,N)
    B = k*v + pow(g,b,N)
    print("C: Sending B")
    server.sendline(str(B))

    #Receiving A 
    print("C: Receiving  A")
    A = int(server.recvline(keepends = False))
    print ("C: Received A",A)

    ##calculating u 
    u = hashlib.sha1(str(A).encode()+str(B).encode()).digest()
    u = Crypto.Util.number.bytes_to_long(u)

    ##calculating shared key 
    Shared_Key_Server = pow(A * pow(v, u, N), b, N)
    print("kserver",Shared_Key_Server)
    ## Receiving M1
    M1 =  str(server.recvline(keepends = False).decode())  
    M1_test = str(hashlib.sha256(str(A).encode()+str(B).encode()+str(Shared_Key_Server).encode()).digest().hex())
     
    if M1 == M1_test:
        print("Connection Verified")
    else:
        print("Connection Terminated")
        return 1
    
    M2 = hashlib.sha256(str(A).encode()+M1.encode()+str(Shared_Key_Server).encode()).digest().hex()

    print("C: Sending  Verification Msg")
    server.sendline(str(M2))
    print ("C: Sent M2")
    print('Connection Established')

if __name__ == "__main__":
   main()

