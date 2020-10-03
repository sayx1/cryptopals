import random   
from set3_18 import *


def randomkey(length:int)->bytes:
    """
    function returns a random key of given length
    param1: length of key (int)
    
    return: key (bytes)
    """
    key = b''
    for i in range(length):
        j = random.randint(1,256)
        key = key + bytes([j])
    return key

def decryption_oracle(ctxt:bytes)->bytes:
    return(ctr_mode(ctxt,key,nonce))

def encryption_oracle(text:bytes)->bytes:
    '''
    '''
    user_data = b''
    for i in text:
        if i == 59 or i == 61:
            continue
        user_data = user_data + bytes([i])
        
    msg_1 = b"comment1=cooking%20MCs;userdata="
    msg_3 = b";comment2=%20like%20a%20pound%20of%20bacon"
    return(ctr_mode(msg_1+user_data+msg_3,key,nonce))

def ctr_bitflipping()->bytes:
    user_data_1 = b'LooL'
    user_data_2 = b'LooLXadminXtrue'
    cipher1 = encryption_oracle(user_data_1)
    cipher2 = encryption_oracle(user_data_2)
    for i in range(len(cipher1)):
        if cipher1[i] != cipher2[i]:
            working_index = i 
            break


    change1 = ord(';') ^ ord('X') ^ cipher2[working_index]
    change2 = ord('=') ^ ord('X') ^ cipher2[working_index+6]


    return(cipher2[:working_index]+bytes([change1])+cipher2[working_index+1:working_index+6]+bytes([change2])+cipher2[working_index+7:])




def main():
    cipher = ctr_bitflipping()
    final = decryption_oracle(cipher)
    print(final)
if __name__ == '__main__':
    key = randomkey(16)
    nonce = 0
    main()

