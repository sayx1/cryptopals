# Break "random access read/write" AES CTR

Say some one has made a web server with AES ctr and you have access to an edit function where you can change what is being encrypted at any place.

```python
edit_oracle(ctxt:bytes,key:bytes,nonce:int,offset:int,nexttext:bytes)
```

What you could do is simply send null bytes with length equal to the ctxt which will give you the key-stream which XORED with ctxt will give you the plaintext.