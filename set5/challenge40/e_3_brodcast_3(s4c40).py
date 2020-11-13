from rsa import * 
from gmpy import invert


msg = b'attack on dawn'
#cipher,e,n = rsa(msg)
c1,n1 = rsa(msg)
c2,n2 = rsa(msg)
c3,n3 = rsa(msg)

ms1 = n2*n3
y1 = c1 * ms1 * invert(n1,ms1)

ms2 = n1*n3
y2 = c2 * ms2 * invert(n2,ms2)

ms3 = n2*n1
y3 = c3 * ms3 * invert(n3,ms3)

mod_prod = n1*n2*n3
result = (y1 + y2 + y3) % mod_prod


decrypt_msg = int(gmpy.mpz(result).root(3)[0].digits())

dec = Crypto.Util.number.long_to_bytes(decrypt_msg)
print(dec)
