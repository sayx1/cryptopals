from time import time
from random import randint 
from set3_21 import MT19937_32


def guess_seed(random_number):
    #choose on the range of deltas we have kept
    initial_guess = int(time()) + 2000
    guess = 0 
    for i in range(1,1000000):
        
        seed = initial_guess -i
        prng =  MT19937_32(seed)
        if next(prng) == random_number:
            guess = seed 
            print('guess:',guess)
            break
    if guess == 0:
        print("couldn't find seed try chaning the conditions")

if __name__ == '__main__':
    current_time = int(time())
    wait1 = randint(40,1000)
    seed = current_time + wait1
    wait2 = randint(40,1000)
    prng = MT19937_32(seed)
    random_number = next(prng)
    guess_seed(random_number)


