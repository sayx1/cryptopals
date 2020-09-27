# Challenge 22: Crack an MT19937 seed

The challenge is quite straight forward we just need to create a random number using seed that is based on the current UNIX time. If the seed we use is predictable and can be guessed efficiently by the attacker than the attacker can easily guess the seed and thus the random number.