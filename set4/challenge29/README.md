# Break a SHA-1 keyed MAC using length extension

When we send the message to the oracle it prepends it with a key and hashes the result. This forms a MAC. The basic idea is to for BOB and Alice to communicate in a way that they both can generate hashes using the MAC and anyone without the message cannot do so thereby ensuring where the message came from.

How SHA1 works is it keeps 5 32 bit numbers which are updated for every block. Say we have a MAC from the original `key+message` this can be used to regenerate the states that form the hash which in turn can be used generate any new hash we want.

We can just rework the way the state is generated to regenerate it.

As all standard ciphers the thing to consider now will be padding. We need to generate padding in a way that is similar to what the actual program would generate on hashing.

`forged_msg = key + original_msg + glue_msg + glue_padding`  

```python
def get_internal_states(msg_digest:bytes)->list:
    a = msg_digest >> 128
    b = (msg_digest >> 96) & 0xffffffff
    c = (msg_digest >> 64) & 0xffffffff
    d = (msg_digest >> 32) & 0xffffffff
    e = msg_digest & 0xffffffff
    
    return ([a,b,c,d,e])
```

We need to modify the implementation of SHA1 so that it can take in the states and compute from there. We also need to modify the function so that it takes the changing length.

![screenshot.png)

We can know just crack it by guessing the key length and sending the injection text, states and the length of forged message.
