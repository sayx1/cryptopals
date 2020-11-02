import random 
known_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
                107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
                167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
                229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353,
                359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
                431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487,
                491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569,
                571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631,
                641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773,
                787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857,
                859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937,
                941, 947, 953, 967, 971, 977, 983, 991, 997] 

def get_bit_number(n):
    return(random.randrange(pow(2,n-1)+1,pow(2,n)-1))


def milan_rabin_test(test_num):
    for i in range(1,(test_num-1)):
        if ((test_num-1)%(2**i)!=0):
            r = i-1
            d = (test_num-1)//(2** (i-1) )
            break
    for k  in range(20):
        a = random.randint(2,test_num-2)
        x = pow(a,d,test_num)
        if (x == 1 or x == test_num-1):
            continue
        for j in range(r-1):
            x = pow(x,2,test_num)
            if (x == test_num-1):
                continue
        return False
    return True

def get_low_level_prime(n):
    while(True):
        test_num = get_bit_number(1024)
        for divisor in known_prime:
            if test_num % divisor == 0:
                break 
        else:
            return test_num

def n_Bit_Prime(n=1024):
    while(True):
        x = get_low_level_prime(1024)
        if (milan_rabin_test(x)):
            return x
            



