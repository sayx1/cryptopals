import hashlib
''' python implementation of pseudocode for SHA1
        https://en.wikipedia.org/wiki/SHA-1#SHA-1_pseudocode
'''


def chunks(text:bytes,blocksize:int)->bytes:
    """
    pram1: whole encrypted messages 
    pram2: amount of chunks needed 

    return array of chunks of data
    """
    chunk_data = b''
    chunks = []
    for i in range(0,len(text),blocksize):
        chunk_data = text[i:i+blocksize] 
        chunks.append(chunk_data)
    return chunks


def SHA_1(message:bytes)->bytes:

    #initilize the variables 
    
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    MAX_WORD = 0xFFFFFFFF
    

    #length of message in bits 
    ml = len(message) * 8
    

    # the message length must be congurent to -64 \eqiv 448 (%512)
    # msg len would have to increnmented 1 as we need to add 1
    # ( len_of_padding + msg_len + 1 ) % 448 = 0
    len_of_pad = - ( ml + 1 + 64) % 512
    

    padded_msg =  message+ bytes([0b10000000]) + b'\x00'*(len_of_pad//8) + ml.to_bytes(8,byteorder='big')
    

    # split the message into 32 bits chunks
    words = [int.from_bytes(w, byteorder='big')
            for w in chunks(padded_msg, 4)]

    
    # this just sperates the list into blocks of 512 bits
    M = chunks(words,16)

    lrot = lambda x, n: ((x << n) | (x >> (32 - n))) 
    def S(X, n):
        'circular left shift (a.k.a "rotate left")'
        # don't forget reduction modulo 2^32 !
        # it is not explicitely written in the formula in the RFC
        # (it is in the prose below it though)
        return ((X << n) | (X >> (32-n))) & MAX_WORD

    def f(t, B, C, D):
        if 0 <= t <= 19:
            return (B & C) | ((~B) & D)
        elif 20 <= t <= 39 or 60 <= t <= 79:
            return B ^ C ^ D
        elif 40 <= t <= 59:
            return (B & C) | (B & D) | (C & D)

    def K(t):
        if 0 <= t <= 19:
            return 0x5A827999
        elif 20 <= t <= 39:
            return 0x6ED9EBA1
        elif 40 <= t <= 59:
            return 0x8F1BBCDC
        elif 60 <= t <= 79:
            return 0xCA62C1D6


    for i in range(len(M)):
        W = M[i]

        for t in range(16, 80):
            W.append( lrot(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16],
                        n=1) & 0xffffffff)

        a, b, c, d, e = h0, h1, h2, h3, h4
        for x in range(80):
            if x <= x <= 19:
                f, k = d ^ (b & (c ^ d)), 0x5a827999
            elif 20 <= x <= 39:
                f, k = b ^ c ^ d, 0x6ed9eba1
            elif 40 <= x <= 59:
                f, k = (b & c) | (d & (b | c)), 0x8f1bbcdc
            elif 60 <= x <= 79:
                f, k = b ^ c ^ d, 0xca62c1d6

            temp = lrot(a, 5) + f + e + k + W[x] & 0xffffffff
            a, b, c, d, e = temp, a, lrot(b, 30), c, d


        
        h0 = (h0 + a) & MAX_WORD
        h1 = (h1 + b) & MAX_WORD
        h2 = (h2 + c) & MAX_WORD
        h3 = (h3 + d) & MAX_WORD
        h4 = (h4 + e) & MAX_WORD

    result = b''.join(H.to_bytes(4, byteorder='big') for H in [h0, h1, h2, h3, h4])

    return result

        

def main():

    message = b'wikipedia is a great resource for pseudocode and i have python to do other stuff'
    
    hashed = SHA_1(message)
    print(hashed)
    test = hashlib.sha1(message).digest()
    print(test)
    



if __name__ == '__main__':
    main()
