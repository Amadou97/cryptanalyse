import fpylll
import numpy as np

m = 36
n = 10
p = 257
a = 2090714372
q = 10
b = (253, 20, 49, 222, 0, 161, 71, 41, 247, 28)

B = fpylll.IntegerMatrix(n, m)

for i in range(0, n):
    for j in range(0, m):
        B[i, j] = pow(a, n * i + j, 0x100000001)

fpylll.LLL.reduction(B)
x = fpylll.CVP.closest_vector(B, b)
print(x)

"""
solution = list()
for i in range(len(x)):
    solution.append(hex(x[i]))

# print(solution)
"""
"""
Matrix = []

for i in range(1, m+1):
    ligne = []
    for j in range(1, n+1):
        ligne.append(pow(a, (n*i) + j, 0x100000001))
    Matrix.append(ligne)

Matrix = np.array(Matrix)

x = np.matmul(b, Matrix.transpose())
for i in range(m):
    x[i] = x[i] % p
print(x)

test = np.matmul(x, Matrix)
for i in range(n):
    test[i] = test[i] % p

print(test)
"""
