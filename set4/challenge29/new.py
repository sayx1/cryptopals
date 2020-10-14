def split_bytes_in_blocks(text:bytes,blocksize:int)->bytes:
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





def sha1_padding(msg, forced_msg_byte_length=None):

    # we are limiting ourselves to messages being byte strings
    # even though specification mentions bit strings of any length
    assert isinstance(msg, bytes)

    # message length in bits
    if forced_msg_byte_length == None:
        msg_length = len(msg)*8
    else:
        msg_length = forced_msg_byte_length*8

    # we must append a "1" bit.
    # since we are always working with bytes
    # the appended bit will always be at the beginning of the next byte

    # computing the number of "zeroes" to append
    # we need msg_length + 1 + m + 64 = 0 mod 512
    # thus m = -(msg_length + 1 + 64) mod 512
    m = -(msg_length + 1 + 64) % 512

    # m+1 will always be a multiple of 8 in our case
    padded_msg = (msg
                  + bytes([0b10000000])
                  + b'\x00'*(m//8)
                  + msg_length.to_bytes(8, byteorder='big')
                 )

    return padded_msg


def SHA_1(msg, state=None, message_added_length=None):
    # following RFC 3174
    # https://tools.ietf.org/html/rfc3174

    # we are prioritizing readability and similarity with the specs
    # over optimization

    # we are always in big-endian form in SHA1
    # (Section 2.c: "The least significant four bits of the integer are
    # represented by the right-most hex digit of the word representation")

    # to use as a bit mask for reduction modulo 2^32
    MAX_WORD = 0xFFFFFFFF

    # Section 3: Operations on Words

    def S(X, n):
        'circular left shift (a.k.a "rotate left")'
        # don't forget reduction modulo 2^32 !
        # it is not explicitely written in the formula in the RFC
        # (it is in the prose below it though)
        return ((X << n) | (X >> (32-n))) & MAX_WORD

    # Section 4: Padding
    
    if message_added_length == None:
        padded_msg = sha1_padding(msg)
    else:
        forced_msg_byte_length = len(msg) + message_added_length
        padded_msg = sha1_padding(msg, forced_msg_byte_length)

    words = [int.from_bytes(w, byteorder='big')
             for w in split_bytes_in_blocks(padded_msg, 4)]

    # "The padded message will contain 16 * n words"
    n = len(words)/16
    print(n)
    assert n.is_integer()
    n = int(n)

    # "The padded message is regarded as a sequence of n blocks M(1), M(2), …"
    M = split_bytes_in_blocks(words, 16)

    # Section 5: Functions and Constants Used

    def f(t, B, C, D):
        if 0 <= t <= 19:
            return (B & C) | ((~B) & D)
        elif 20 <= t <= 39 or 60 <= t <= 79:
            return B ^ C ^ D
        elif 40 <= t <= 59:
            return (B & C) | (B & D) | (C & D)
        else:
            raise Exception('t must be between 0 and 79 inclusive')

    # this could be optimized, for instance with an array
    # but this way is closer to how it is described in the specs
    def K(t):
        if 0 <= t <= 19:
            return 0x5A827999
        elif 20 <= t <= 39:
            return 0x6ED9EBA1
        elif 40 <= t <= 59:
            return 0x8F1BBCDC
        elif 60 <= t <= 79:
            return 0xCA62C1D6
        else:
            raise Exception('t must be between 0 and 79 inclusive')

    # Section 6: Computing the Message Digest
    # Using "method 1" (Section 6.1)

    if state == None:
        H0 = 0x67452301
        H1 = 0xEFCDAB89
        H2 = 0x98BADCFE
        H3 = 0x10325476
        H4 = 0xC3D2E1F0
    else:
        # SHA-1 state cloning
        assert isinstance(state, tuple)
        assert len(state) == 5
        assert all(isinstance(x, int) for x in state)

        H0, H1, H2, H3, H4 = state

    for i in range(len(M)):
        W = M[i]
        assert len(W) == 16
        
        for t in range(16, 80):
            W.append( S(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16],
                        n=1) )

        A, B, C, D, E = H0, H1, H2, H3, H4

        for t in range(80):
            TEMP = (S(A, 5) + f(t, B, C, D) + E + W[t] + K(t)) & MAX_WORD

            E = D; D = C; C = S(B, 30); B = A; A = TEMP

        H0 = (H0 + A) & MAX_WORD
        H1 = (H1 + B) & MAX_WORD
        H2 = (H2 + C) & MAX_WORD
        H3 = (H3 + D) & MAX_WORD
        H4 = (H4 + E) & MAX_WORD

    result = b''.join(H.to_bytes(4, byteorder='big') for H in [H0, H1, H2, H3, H4])

    return result
