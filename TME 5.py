import fpylll as lll

p = 0xffffffffffffffffffffffff1
entiers = (0xc6d38accf8ee14ba1d6dee069,  0xa8c20c33fc892060b5ded9411,  0xc1cff492a26c0133a9f139dff,
          0x10608ed9f6d7fcf30a042f99b,  0x358356c7c75141134cc3cec7c,  0x6d687a378293cee55af7693db,
          0x590b15c5a3110d47c38774432,  0x3c5ee07ace81595c08b42a186,  0xcbc0c67aba6c418b464262400,
          0xb128b3a8b77ff5df2bf41ca70,  0x88db009e0da402bac96246d34,  0xddac8beb19ce8c2f26884b7fb,
          0xa46a98b6275d4a39a8600a3f2,  0x89d866ccf0d1dfb28e32f989c,  0x8d3fbfc51ff9a2e19def1804d,
          0x49aada71bac845b05f0515a4c,  0x7d98766f277e59091f31d8d87,  0xd69ea57212904c5c545a56337,
          0x24b9ec58a0ae93553f105964c,  0xdeb09430e07ff68d1198199b7,  0xefcd0027c7f2fe2c7b787dbb1,
          0xde2e155b563830e1525b2c43a,  0xa7e41c62c201e6254ca5f7807,  0xd7c9d82afd3274a06fcad9468,
          0x159b85d8989fee67a95222076,  0x9b9a67df575503c20cf90b5ec,  0x0f5e39ed43bcd87443702fe90,
          0x48225bdbf9ce978a85928b9d6,  0x23b378254fe06b4539a44bf3f,  0x2ae3f8975d1eeed3e4b2f4299,
          0x62a856b8d10b544c5fac4dbff,  0xa9d07cf7bbd68b5be2705006a,  0x1e609c9eae38b2184004db321,
          0xe918e08af78702da832a3f07a,  0x92b9a57aaa3159a172b0edb59,  0xc73f9f2cdc47108fea112772a,)


n = len(entiers)
A = lll.IntegerMatrix(n + 1, n + 1)

for i in range(1, n + 1):
    A[i, i] = 1
    A[i, 0] = entiers[i - 1]

A[0, 0] = p

t = (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
#t = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

lll.LLL.reduction(A)

x = lll.CVP.closest_vector(A, t)
res = [entiers[i] * (x[i+1]) for i in range(n)]
print(sum(res) % p)
print(x)

for nb in res:
    if nb: print(hex(nb), end=', ')

print('')
