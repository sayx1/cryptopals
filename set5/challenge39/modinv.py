# Took from SO
def egcd(a, b):
    if b == 0:
       d,x,y = a,1,0
    else:
        (d,p,q) = egcd(b,a%b)
        x = q
        y = p - q * (a//b)
    assert a % d == 0 and b % d == 0
    assert d == a*x + b*y
    return (d,x,y)

def modinv(a,m):
    g,x,y = egcd(a,m)
    if g != 1:
        print("Modular Inverse Doesn't exit")
    else:
        return x%m

print(modinv(17,3120))
