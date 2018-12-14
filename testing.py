!/usr/bin/env python

import bitcoin
import hashlib
import random

def ecdsa_sign_k(z, d, k):
    r, y = bitcoin.fast_multiply(bitcoin.G, k)
    s = bitcoin.inv(k, bitcoin.N) * (z + r*d) % bitcoin.N
    v, r, s = 27+((y % 2) ^ (0 if s * 2 < bitcoin.N else 1)), r, s if s * 2 < bitcoin.N else bitcoin.N - s
    return v, r, s

# Generate secret key & the corresponding public key and address
sk = random.SystemRandom().randrange(1, bitcoin.N)
Q = bitcoin.fast_multiply(bitcoin.G, sk);

# Sign 2 differents messages with same k
signing_k = random.SystemRandom().randrange(1, bitcoin.N)
z1 = bitcoin.hash_to_int(hashlib.sha256('first_message').hexdigest())
z2 = bitcoin.hash_to_int(hashlib.sha256('second_message').hexdigest())
v1, r1, s1 = ecdsa_sign_k(z1, sk, signing_k)
v2, r2, s2 = ecdsa_sign_k(z2, sk, signing_k)
assert r1 == r2
print('+ R used   = {:x}'.format(r1))

# Calculate k candidates
k_candidates = [
    (z1 - z2) * bitcoin.inv(s1 - s2, bitcoin.N) % bitcoin.N,
    (z1 - z2) * bitcoin.inv(s1 + s2, bitcoin.N) % bitcoin.N
]
for k in k_candidates:
    priv_key = (s1 * k - z1) * bitcoin.inv(r1, bitcoin.N) % bitcoin.N
    if bitcoin.fast_multiply(bitcoin.G, priv_key) == Q:
        print('+ Calc key = {0}'.format( priv_key ))
        break
else:
    print('An unknown error occured.')
