import functools
import operator
from hashlib import sha256


def XOR(*seqs):
    return bytearray([functools.reduce(operator.xor, t, 0) for t in zip(*seqs)])


def feistel(text, K, w, debug=0):
    k = []
    for i in range(0, 16, 4):
        k.append(K[i:i + 4])

    L = text[0:16]
    R = text[16:32]

    if w == 'Enc':
        h0 = sha256(k[0] + R).digest()[:16]  # [:16] == 8 bytes == 64 bits...
        L = XOR(L, h0)

        h1 = sha256(k[1] + L).digest()[:16]
        R = XOR(R, h1)
        # '''
        h2 = sha256(k[2] + R).digest()[:16]
        L = XOR(L, h2)

        h3 = sha256(k[3] + L).digest()[:16]
        R = XOR(R, h3)
        # '''

        # ciphertext = L+R

    elif w == 'Dec':
        # '''
        h3 = sha256(k[3] + L).digest()[:16]
        R = XOR(R, h3)

        h2 = sha256(k[2] + R).digest()[:16]
        L = XOR(L, h2)
        # '''
        h1 = sha256(k[1] + L).digest()[:16]
        R = XOR(R, h1)

        h0 = sha256(k[0] + R).digest()[:16]  # [:16] == 8 bytes
        L = XOR(L, h0)

        # plaintext = L+R

    else:
        exit("'Enc' to encrypt, 'Dec' to decrypt")

    return L, R


''' # Feistel Network ok (Encryption and Decryption)
key = b'0001020304051617'

XL = b'0000000000000000'
YL = b'1111111111111111'
R = b'08090a0b0c0d0e0f'

X = XL+R
Y = YL+R 

X4L, X4R = feistel(X, key, 'Enc')
print(X4L+X4R)
t = bytearray(b'\x98\xadHBFE[(\xed\xe2(?<\xdeo\x7f\x1d\xd8uqV\x97\x9e\xe63w\xc8\xfb\x08F\xad\xbc')
X4L, X4R = feistel(t, key, 'Dec')
print(X4L+X4R)
'''

'''
Last feistel round
'''


def lastFeistelRound(text, keyTest, w):
    L = text[0:16]
    R = text[16:32]
    if w == 'Enc':  # ???
        h3 = sha256(keyTest + L).digest()[:16]
        R = XOR(R, h3)
    elif w == 'Dec':  # ok
        h3 = sha256(keyTest + L).digest()[:16]
        R = XOR(R, h3)
    return L, R


"""
1) Request the encryption of 2 messages X = (XL, R) and Y = (YL, R) 
to obtain X4 = (X4L, X4R) and Y4 = (Y4L, Y4R). 

2) For each possibility of key k4 (1 to 2**16)
Reverse a feistel round on X4 and Y4 using the possibility of k4 to obtain X3 and Y3

3) Form the new cipher of the 3 turn distinguisher as Z3 = (Y3L, Y3R xor XL xor YL)

4) Do a new feistel round using the k4 possibility on Z3 to get Z4

5) Pass Z4 to the deciphering oracle to decipher Z4 into Z = (ZL, ZR)

6) If good value of k4 to undo and redo the last round 
   Then property (ZR == Y3L xor X3L xor R) satisfied & X3 and Y3 correct

   Else bad value of k4 --back to--> 2)
"""


def feistelAttack():
    key = b'0001020304051617'

    # 1)
    XL = b'0000000000000000'
    YL = b'1111111111111111'
    R  = b'08090a0b0c0d0e0f'

    X = XL + R
    Y = YL + R

    X4L, X4R = feistel(X, key, 'Enc')  # oracle
    X4 = X4L + X4R
    # print('X4 :', X4)

    Y4L, Y4R = feistel(Y, key, 'Enc')  # oracle
    Y4 = Y4L + Y4R
    # print('Y4 :', Y4)

    # 2)
    '''for trial in range(1, 2**16):'''
    trial = '1617'  # The correct 'trial' for the 4th key
    '''trial = hex(trial)[2:].zfill(4)'''

    keyTest = trial.encode()

    # Reverse Feistel last round
    X3L, X3R = lastFeistelRound(X4, keyTest, 'Dec')  # not oracle
    Y3L, Y3R = lastFeistelRound(Y4, keyTest, 'Dec')  # not oracle
    '''
    X3 = X3L+X3R 
    print('X3 :', X3)
    Y3 = Y3L+Y3R 
    print('Y3 :', Y3)
    '''

    # 3)
    # The new cipher for the 3 round distinguisher
    Z3 = Y3L + XOR(Y3R, XL, YL)
    # print('Z3 : ', Z3)

    # 4)
    # re-make the last round
    Z4L, Z4R = lastFeistelRound(Z3, keyTest, 'Enc')  # not oracle
    Z4 = Z4L + Z4R

    # 5)
    ZL, ZR = feistel(Z4, key, 'Dec')  # oracle

    # 6) Verification
    '''
    if ZR == XOR(Y3L, X3L, R):
        print(ZR)
        print(XOR(Y3L, X3L, R))
        break
    '''
    print(ZR)
    print(XOR(Y3L, X3L, R))


feistelAttack()

"""
i

tmp = f_i(R_i, k_i)
L_i+1 = R_i
R_i+1 = xor(tmp, L_i)


*i = 0*

h0 = f_0(R_0, k_0)
L_1 = R_0
R_1 = xor(tmp, L_0)

*i = 1*

h1 = f_1(R_1, k_1)
L_2 = R_1
R_2 = xor(tmp, L_1)

*i = 2*

h2 = f_2(R_2, k_2)
L_3 = R_2
R_3 = xor(tmp, L_2)

*i = 3*

h3 = f_3(R_3, k_3)
L_4 = R_3
R_4 = xor(tmp, L_3)

out_L = R_4
out_R = L_4
"""

'''
Test of the Distinguisher for a 2-round Feistel network
'''


def test2roundFeistelDistinguisher():
    key = b'0001020304050607'

    XL = b'0000000000000000'
    YL = b'1111111111111111'
    R = b'08090a0b0c0d0e0f'

    X = XL + R
    Y = YL + R

    X2L, X2R = feistel(X, key, 'Enc')

    Y2L, Y2R = feistel(Y, key, 'Enc')

    # Should be equal for a 2-round Feistel network => ok
    print(XOR(X2L, Y2L))
    print(XOR(XL, YL))


test2roundFeistelDistinguisher()  # (have to change the feistel network above)
