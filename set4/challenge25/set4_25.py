from set3_18 import *
import base64
import os
import random 

def encrypt(plain_text:bytes)->bytes:
    '''encrypt files under ctr mode 
    '''
    cipher = ctr_mode(plain_text,key,nonce)
    return(cipher)


def edit_oracle(ctxt:bytes,offset:int,nexttext:bytes)->bytes:
    ''' change certian part of cipher text(from certian offset i.e if offset = 10
        cipher text from [10:len(changed_text)] is changed) to the text you like.
        attacker only has access to edit function and can send cipher,offset and
        newtext to change 

        param1 -> cipher text 
        param2 -> offset 
        param3 -> text to change to
        
        return -> edited cipher text 
    '''
    key_stream = ctr_keystream(key,nonce)
    random_str = b'AAAAA' * len(ctxt)
    keystream = xor_chunks(random_str,ctr_mode(random_str,key,nonce))
    new_chunk = xor_chunks(nexttext,keystream[offset:offset+len(nexttext)])
    result = ctxt[:offset] + new_chunk + ctxt[offset+len(nexttext):]
    return result 


def main():
    fhandle = open('ctxt','r')
    text = fhandle.read().split('\n')
    text = b''.join(list(map(base64.b64decode,text[:-2])))
    cipher = encrypt(text)
    keystream = edit_oracle(cipher,offset=0, nexttext=b'\x00'*(len(cipher)))
    
    final = xor_chunks(cipher,keystream)
    
    if final == text:
        print('yess')

    
if __name__ == '__main__':
    BLOCK_SIZE = 16
    key = b'YELLOW SUBMARINE'
   
    nonce = 0
    main()
