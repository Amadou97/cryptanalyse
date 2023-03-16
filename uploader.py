############################################################################################################
import base64
import fpylll
from fpylll import *
import string
from aes import *


def int2str(m):
    size = len(str(m))
    print("".join([chr((m >> j) & 0xff) for j in reversed(range(0, size << 3, 8))]))


'''
Hash function
M : bytes encoded string

1. [initialisation] Poser hash <--- 0 et i <--- 0.
2. [Fini ?]         Si i == |M|, renvoyer hash et s'arrêter.
3. [Prochain octet] Calculer hash <--- (65599 * hash + M[i]) modulo 2**128. 
                    Incrémenter i puis retourner à l'étape 2.
'''


def SDBM(M):
    h = 0
    i = 0
    while i < len(M):
        m = int(M[i:i + 2], 16)
        h = (65599 * h + m) % pow(2, 128)
        i += 2
    return hex(h)[2:]

'''
with open('/home/bayo/PycharmProjects/CRYPTA/moi.txt', 'r') as f:
    M = f.read()

M.replace("\n", "")
M = "".join(M.split('\n'))
M = base64.b16decode(M) #to_bytes
print(SDBM(M.hex()))
'''

'''
>>> key = base64.b16decode("00000000000000000000000000000000")
>>> a = AES(key)
>>> plaintext = base64.b16decode("80000000000000000000000000000000")
>>> ciphertext = base64.b16decode("3ad78e726c1ec02b7ebfe92b23d9ec34", casefold=True)
>>> assert a.encrypt(plaintext) == ciphertext
'''

'''
M : Message ASCII
K : Key, hex value (str)
'''


def tarMAC(M, K):
    H = SDBM(M).upper()
    print("hash message : ", H)
    key = base64.b16decode(K)  # to_bytes
    a = AES(key)
    plaintext = base64.b16decode(H)  # to_bytes
    tag = a.encrypt(plaintext)
    return tag.hex()


'''
M : bytes encoded message
K : seed (128 bits)
'''


def TLCG(M, K):
    cipher = ''
    i = 0
    M = M.hex()

    x = K
    while i < len(M):
        Y = x // 2 ** 120

        P = int(M[i:i + 2], 16)

        C = hex(Y ^ P)[2:].zfill(2)

        cipher += C
        x = (x * 47026247687942121848144207491837523525) % 2 ** 128
        i += 2

    return cipher.upper()


'''
M = "Les sanglots longs\nDes violons\nDe l'automne\nBlessent mon coeur\nD'une langueur\nMonotone."
M = M.encode()
K = 0x71d05909e13748ff733ffccfbfbf40eb
print(TLCG(M, K))
#cipher correct ==
#3D8A065B3CCBA48C74C53C4B9D7DBBBCC1B3BA9C8AE689687A31517B3BD79814B133A3B6671124E8BAE01EFBA766C3EBD9F6908E650
#00995A99A873CD085BFEADA8DB8E6565539B1FFB3F703F386B41C2D37F2BB5B351C
'''


def TLCG_attack():
    f = open("moi.txt", "r")
    msg = f.read().replace("\n", "")

    g = open("robot.rml", "r")
    msg_robot = g.read().replace(" \n", "\n")

    msg_dec = base64.b16decode(msg)
    msg_robot_dec = msg_robot.encode('ascii')

    flux = []
    for a, b in zip(msg_dec, msg_robot_dec):
        flux.append(a ^ b)

    n = 19
    z = [flux[i] * pow(2, 120) for i in range(n)]

    # on veut la matrice suivante :
    # [ 1,      a,   a**2,   a**3, ..., a**(n-1) ]
    # [ 0, 2**128,      0,      0, ...,        0 ]
    # [ 0,      0, 2**128,      0, ...,        0 ]
    # [ 0,      0,      0, 2**128, ...,        0 ]
    # [..........................................]
    # [ 0,      0,      0,      0, ...,   2**128 ]

    mat = [[0 for j in range(n)] for i in range(n)]

    a = 47026247687942121848144207491837523525
    mod = pow(2, 128)
    for i in range(n):
        for j in range(n):
            mat[i][i] = mod
            mat[0][j] = pow(a, j, mod)

    # print(mat)
    # print(z)

    reseau = IntegerMatrix.from_matrix(mat)
    reseau = fpylll.LLL.reduction(reseau)

    x = fpylll.CVP.closest_vector(reseau, z)
    graine = x[0]
    print(hex(graine))


# TLCG_attack()


def TLCG_decypt(C, K):
    plaintext = ''
    i = 0
    C = C.hex()
    x = K  # seed
    while i < len(C):
        Y = x // 2 ** 120  # MSB
        c = int(C[i:i + 2], 16)  # cipher
        P = hex(Y ^ c)[2:].zfill(2)  # plain
        plaintext += P
        x = (x * 47026247687942121848144207491837523525) % 2 ** 128  # state
        i += 2
    plaintext = int(plaintext, 16)
    return int2str(plaintext)


'''
with open('/home/bayo/PycharmProjects/CRYPTA/moi.txt', 'r') as f:
    C = f.read()
C = "".join(C.split('\n'))
C = base64.b16decode(C)  # to bytes
K = 0xd8f731df6828f5846f5c07f9cb3ef3d3
TLCG_decypt(C, K)
print("end")
'''


def SDBM_attack(M_1, M_2, asciNum):
    '''
    Search for a suffix to forge a message (RML code)
    which has the same SDBM_hash 'h' than a valid message
    Thus we obtain a correct tarMAC
    '''

    #M.replace("\n", "")
    M_1 = "".join(M_1.split('\n'))
    M_1 = base64.b16decode(M_1)  # to_bytes

    #h = SDBM(M_1.encode("utf-8").hex())
    h = SDBM(M_1.hex())
    print(h)
    h_int = int(h, 16)
    n = 21  # n must be >= 16
    # building the lattice
    """
     [ 1,  0,  0,  0, ...,  0,  0,  a**(n-1) ]
     [ 0,  1,  0,  0, ...,  0,  0,  a**(n-2) ]
     [ 0,  0,  1,  0, ...,  0,  0,  a**(n-3) ]
     [.......................................]
     [ 0,  0,  0,  0, ...,  1,  0,         a ]
     [ 0,  0,  0,  0, ...,  0,  1,         1 ]
     [ 0,  0,  0,  0, ...,  0,  0,    2**128 ]
    """

    # Initializing G
    G = [[0 for i in range(n + 1)] for j in range(n + 1)]
    a = 65599
    # last column
    for i in range(1, n + 1):
        G[i - 1][n] = a ** (n - i)

    # diagonal
    for i in range(n):
        G[i][i] = 1

    # just before last element
    G[n - 1][n] = 1
    # last element
    G[n][n] = 2 ** 128
    target = [asciNum for i in range(n + 1)]  # someties ok with 80 (pay attetion on non-ascii chars in the suffix)...
    SDBM_M_2 = int(SDBM(M_2.encode().hex()), 16)
    verif = (h_int - SDBM_M_2 * a ** n) % 2 ** 128  # n == len(suffix)
    print('verif :', verif)  # hex(verif).lstrip('0x'))
    target[-1] = verif  ###### !!!!!!!!!! ########
    target = tuple(target)
    ##### LLL #####
    G = IntegerMatrix.from_matrix(G)

    LLL.reduction(G)
    res = CVP.closest_vector(G, target)  # res == (S_0, ..., S_{n-1}, h)
    print(res)
    res = list(res)
    for j in range(128):
        res[-2] = j
        rsum = 0
        for i in range(n):
            rsum = (rsum + a ** (n - 1 - i) * res[i]) % 2 ** 128
        print('sum :', rsum)
        if rsum == verif:
            print(j)
            res[-2] = j  # found by bruteforce to have 'verif' as the last element
            break

    print(res)
    suffix = ''
    for e in res[:-1]:
        suffix += chr(e)

    print(suffix)
    print('len_suffix :', len(suffix))

    # Check if there are unprintable ascii chars
    filtered_suffix = filter(lambda x: x in string.printable, suffix)
    cpt = 0
    for e in filtered_suffix:
        cpt += 1
    print('len_filtered_suffix :', cpt)
    if cpt != n:
        asciNum += 1
        SDBM_attack(M_1, M_2, asciNum)
        return
    else:
        print('Good printable chars, with asciNum =', asciNum)
    # SDBM(suffix) =?= (h - SDBM(M_2) * 65599**len(suffix)) % 2**128
    SDBM_suffix = SDBM(suffix.encode().hex())
    print('suffix : ', suffix)
    print('SDBM_suffix :', SDBM_suffix)
    print('verif :', hex(verif).lstrip('0x'))
    print('equal ? :', verif == int(SDBM_suffix, 16))
    # SDBM((M_2+suffix).encode()) =?= h
    final = M_2 + suffix
    # print(final)
    SDBM_final = SDBM(final.encode().hex())
    print('SDBM(M2 || suffix) :', SDBM_final)
    print('SDBM(M1) :', h)
    print('equal ? :', h == SDBM_final)


with open('/home/bayo/PycharmProjects/CRYPTA/moi.txt', 'r') as f:
    M_1 = f.read()
with open('/home/bayo/PycharmProjects/CRYPTA/reponseRML.rml', 'r') as f:
    M_2 = f.read()
M_1 = M_1.rstrip('\n')  # '\n' added by f.read()
M_2 = M_2.rstrip('\n')  # '\n' added by f.read()
asciNum = 64
SDBM_attack(M_1, M_2, asciNum)

# `-----END RML PROGRAM -----'
# Encryption: [TLCG]
# hash: [SDBM] 59afb0b9135fb6c70bac3696102754a2
# MAC: [tarMAC, 17553 bytes] dfd2cdf1ef9ad4d2dd4692da02ff1e42
