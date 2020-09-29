
state = list()
def MT19937_32(seed=5489):
        """
        python impletation using wikipeida's pseudocode
        https://en.wikipedia.org/wiki/Mersenne_Twister
        https://cedricvanrompay.gitlab.io/cryptopals/challenges/21.html
        """
        #parameters as given in wikipedia
        (w, n, m, r) = (32, 624, 397, 31)
        a = 0x9908B0DF
        (u, d) = (11, 0xFFFFFFFF)
        (s, b) = (7, 0x9D2C5680)
        (t, c) = (15, 0xEFC60000)
        l = 18
        f = 1812433253
        
        # (w-r) number of 1's at LSB
        higher_mask = ((1<<w) - 1) - ((1<<r) - 1)
        # (r) number of 1's at LSB
        lower_mask = (1<<r)-1
        
        #initilize generator with seed 
        
        state.append(seed)
        for i in range(1,n):
            prev = state[-1]
            #truncates x into 32 digits by property of logical operator and
            x = (f * (prev ^ (prev >> (w-2))) + i) & d 
            state.append(x)


        def twist(x):
            return (x >> 1)^a if (x % 2 == 1) else x >> 1

        while True:
            x = state[m] ^ twist((state[0] & higher_mask) + (state[1] & lower_mask))
            print(x)

            # tempering transform and output to generate the matrix
            y = x ^ ((x >> u) & d)
            y = y ^ ((y << s) & b)
            y = y ^ ((y << t) & c)
            yield y ^ (y >> l)

            # note that it's the 'x' value
            # that we insert in the state
            state.pop(0)
            state.append(x)


def get_state():
    return state

