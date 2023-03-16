import fpylll as lll
from numpy.linalg import norm

n = 7
a = 0x7e96b807802819a1
p = 0xefbdd9cae96f21d4
L = pow(2, 56.19)


A = lll.IntegerMatrix(n, n)

for i in range(1, n):
    A[i, i] = p
    A[0, i] = pow(a, i, p)

A[0, 0] = 1

x = lll.SVP.shortest_vector(A)
print(norm(x) < L)

#print(x)
xx = [hex(a) for a in x]
print(xx)


