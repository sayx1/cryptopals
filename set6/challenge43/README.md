# DSA key recovery from nonce

## DSA how messages are signed and verified?

### First we generate the key parameters,

![images/Untitled.png](images/Untitled.png)

### Each user who sign the message generate, Per-user keys

![images/Untitled%201.png](images/Untitled%201.png)

## Signing

Public Key = (p,q,alpha,y)

Private Key = (x)

![images/Untitled%202.png](images/Untitled%202.png)

## Verifying

![images/Untitled%203.png](images/Untitled%203.png)

# Key Recovery

If we have the signature we can recover the private key as follows,

![images/2020-11-17_11-54.png](images/2020-11-17_11-54.png)
