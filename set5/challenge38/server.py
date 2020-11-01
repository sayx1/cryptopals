import hashlib
import Crypto.Util.number
import random
from pwn import *
k = 3
g = 2
N = 6277101735386680763835789423207666416083908700390324961279
users = {}




def main():
    #Receiving Public key
    server = listen(1234)
    """
    I = str(server.recvline(keepends = False))
    s = str(server.recvline(keepends = False))
    v = int(server.recvline(keepends = False))
    create_users(I,s,v)
    """
    salt = 'YELLOW SUBMARINE'
    v = 3369995099942534326296793450511909312465369947092814340247
    #Communication 
    print("C: Receiving  I")
    username =  str(server.recvline(keepends = False))
    I = username
    print("C: Received I")

    #Receiving A 
    print("C: Receiving  A")
    A = int(server.recvline(keepends = False))
    print ("C: Received A")
    
    # Sending B
    b = random.randint(1,N)
    B = pow(g,b,N)
    print("C: Sending B")
    server.sendline(str(B))
    
    # Sending Salt
    print("C: Sending salt")
    server.sendline(str(salt))
    print("Salt Sent")


    ##sending u
    print("Sending u ")
    u = random.getrandbits(128)
    server.sendline(str(u))
    print("u Sent")

    ##calculating shared key
    s = pow(A * pow(v, u, N), b, N)
    Shared_Key_Server = hashlib.sha256(str(s).encode()).digest().hex()

    
    print("C: Receving  Verification Msg")
    K_test = server.recvline(keepends=False).decode()
    print ("C: Received Verification Message")
    
    if Shared_Key_Server == K_test:
        print('Connection Established')
    else:
        print("K Server ",Shared_Key_Server)
        print("K test ",K_test)
        print("Nice Try, Connection Terminated")


if __name__ == "__main__":
   main()

