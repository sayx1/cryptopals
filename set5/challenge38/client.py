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
    x = hashlib.sha256(salt.encode()+password.encode()).digest()
    x = Crypto.Util.number.bytes_to_long(x)
    v = pow(g,x,N)
    return I,v,x
def main():
    I,v,x = generate_salt_password()
    print("v ",v) 
    send_port = 1234
    r = remote('localhost', send_port)
    """ 
    ##  REGISTRATION
    print("C: Sending Username")
    r.sendline(str(I))
    print("C: Sending Salt")
    r.sendline(str(s))
    print("C: Sending verifier")
    r.sendline(str(v))
    """

    ### Setting Up Connection
    a = random.randint(1,N)
    print("C: Sending Username")
    r.sendline(str(I))

    ##sending A
    print("C: Sending A")
    A = pow(g,a,N)
    r.sendline(str(A))

    ##getting B
    print("C: Receiving  B")
    B = int(r.recvline(keepends = False))
    print ("C: received B")
   
    ##getting salt
    print("C: Receiving salt")
    salt = str(r.recvline(keepends= False))
    print("C: received salt")

    ##getting u 
    print("C: Receiving u")
    u = int(r.recvline(keepends=False))
    print("Received u ")

    #Calculation of Shared Key
    s = pow(B,a+(u*x),N)
    Shared_Key_Client = hashlib.sha256(str(s).encode()).digest().hex()

    

    print(Shared_Key_Client)
    print("C: Sending M1")
    r.sendline(str(Shared_Key_Client))
    
  
if __name__ == "__main__":
   main()

