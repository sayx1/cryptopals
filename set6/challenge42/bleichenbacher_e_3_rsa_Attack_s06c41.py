from rsa import *
from hashlib import sha1
from Crypto.Util.number import long_to_bytes, bytes_to_long
import gmpy2

sha1_asn1 = b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'

def verify_sig(signature,message,pk):
    #generate clearsig
    e,n = pk
    #generate clearsignature
    clearsig = pow(signature,e,n)
    clearsig = b'\x00' + long_to_bytes(clearsig)

    
    # verify if the signature start with 
    # 00 01 FF
    if clearsig[0:3] != b'\x00\x01\xff':
        raise ValueError("No sig marker")

    sep_index = clearsig.index(b'\x00',2)

    if not clearsig[sep_index+1:].startswith(sha1_asn1):
        raise ValueError("no asn1")

    signature_hash = clearsig[sep_index+len(sha1_asn1)+1:sep_index+len(sha1_asn1)+1+20]

    message_hash = sha1(message).digest()

    if message_hash != signature_hash:
        raise ValueError("hashes don't match")

    return True

def forgeSignature(msg,pk):
    e,n = pk

    #creating the hash of the message 
    msg_hash = sha1(msg).digest()
    garbage = b'\x00'*75

    #appending garbage value to forge message we like 
    forged_signature = b'\x00\x01\xff\x00' + sha1_asn1 + msg_hash + garbage
    

    forged_signature_num = bytes_to_long(forged_signature)
    (cube_root,exact) = gmpy2.iroot(forged_signature_num,3)
    cube_root += 1

    recovered = long_to_bytes(pow(int(cube_root),e,n))
    assert b"\x01\xff" in recovered
    assert sha1_asn1 in recovered
    assert msg_hash in recovered

    return int(cube_root)




def main():
    d,e,n = generate_keys()
    msg = b'hello mom'
    private_keys = e,n
    
    forged_signature = forgeSignature(msg,private_keys)
    if(verify_sig(forged_signature,msg,private_keys)):
        print("verfied")

main()
