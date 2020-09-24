# Challenge 20 : Break fixed-nonce CTR statistically

First let's get started first let's just encrypt the given base64 encoded strings with a constant nonce. 

```python
def encrypted_text()->list:
    nonce = 0 
    key = b'YELLOW SUBMARINE'
    fhandle = open('ctxt','r')
    text = fhandle.read().split('\n')[:-1]
    text = list(map(base64.b64decode,text[:]))
    ciphers = [ctr_mode(i,key,nonce) for i in text]
    return ciphers

if __name__ == '__main__':
    BLOCK_SIZE = 16
    ciphers = encrypted_text()
```

Now as all the strings have been encrypted with a constant nonce the problem becomes that of repeating key xor. Since all the strings will be encrypted with same key we can just use the code from previous exercise to solve this. As suggested first we truncate the text to the that of the lowest length of cipher text. than 

```python
key_size = min([len(i) for i in ciphers])
    working_cipher = b''
    working_ciphers = [i[:key_size] for i in ciphers]
    working_cipher = b''.join(working_ciphers)
```

Now we need to work on breaking repeating key xor. First thing we do is assume the key length to be the size of the lowest ciphertext than we make blocks of ciphertext such that each byte with encrypted with a byte fall into the same group.

```python
def breaking_repeating_xor(cipher_txt:bytes,key_size:int)->bytes:
    possible_key = b''

    for i in range(key_size):
        block = b''
        for j in range(i,len(cipher_txt),key_size):
            block += bytes([cipher_txt[j]]) 
        possible_key += break_single_key_xor(block)
    return possible_key
```

Now we take the blocks as they have been encrypted with same byte we can, brute force the cipher text by xor with all in the range of 256 and using frequency analysis to determine if the code is in English language and selecting one that is.

```python
def freq_score(txt:str)->int:
    englishLetterFreq = {'a': .08167, 'e': .12702,  'o': .07507, 't': .09056,
         ' ': .23}
     return sum([englishLetterFreq.get(chr(byte), 0) for byte in txt.lower()])

def break_single_key_xor(cipher_txt:bytes):
    x = [xor_chunks(cipher_txt,bytes([i])*len(cipher_txt)) for i in range(256)]
    scores = [freq_score(x[i]) for i in range(256)]

    return bytes([scores.index(max(scores))])
```