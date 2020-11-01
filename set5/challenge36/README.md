# Secure Remote Password Protocol

→ augmented password-authenticated key agreement (PAKE) protocol 

→ MITM attack is not possible 

→ Basically Alice demonstrates to Bob that Alice is well Alice but no password is shared and even if someone is in the middle Eve cannot do anything.

→ this  is zero-knowledge password proof (ZKPP). a fancy mathematical way of saying I know the password and proving it but not giving out the actual password.

### Protocol

First we Alice needs to establish a password with Bob,

→ First Alice picks a Salt (`s`) and a password (`p`)

→ Then computes x such that `x` = `H(s,p)` where H() is a hash functions 

→ Then compute a host's password verifier v such that `v = g^x` 

( Some implementations can use 

x = `H ( s + I + p )` where I is identifying username or 

x = H ( s | `H ( I + ":" + p )` ) 

so server cannot determine if user share the  same password )

### Registration

`Client` → using salt, password generate `v` such that `v = g^x` and x = H(sat | I | password), this is sent to the server and communicated.

### Establishing Connection

`Client` → send `I` and `A = g^a`

`Server` → send `s` and `B = kv + g^b` where `k = 3` or `k = H(N,g)` 

`Client` and `Server` u = `H ( A , B )`

`Client` →Shared Key Client = ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20%28B-k*g%5Ex%29%5E%7B%28a%20&plus;%20ux%29%7D%20%3D%20%28kv%20&plus;%20g%5Eb-kg%5Ex%29%5E%7B%28a%20&plus;%20ux%29%7D%20%3D%20%28kg%5Ex-kg%5Ex%20&plus;%20g%5Eb%29%5E%7B%28a%20&plus;%20ux%29%7D%20%3D%20%28g%5Eb%29%5E%7B%28a%20&plus;%20ux%29%7D)

`Client` → `H ( Shared Key Client )`

`Server` → Shared Key Server = ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20%28g%5Eav%5Eu%29%5Eb%20%3D%20%5Bg%5Ea%28g%5Ex%29%5Eu%5D%5Eb%20%3D%20%28g%5E%7Ba%20&plus;%20ux%7D%29%5Eb%20%3D%20%28g%5Eb%29%5E%7B%28a%20&plus;%20ux%29%7D)

`Server` → `H ( Shared Key Server)`

`H(Shared Key Client)` = `H(Shared Key Server)`

After generating the key, now both must prove that they have the same shared key.

`Client` → `M1 = H (A | B | Shared Key Client )` to server for verification

`Server` → `M2 =  H (A | M1 | Shared Key Server)` to client for verification.
