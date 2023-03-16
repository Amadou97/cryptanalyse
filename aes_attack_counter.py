import base64
from aes import *

'''
1. [Initialisation.]   Poser CTR <-- IV.
2. [Nouveau bloc.]     Former un bloc P de 16 octets en représentant l'entier 
                       CTR au format "big-endian".  Faire C <-- AES-128(Kaes, P) 
                       et i <-- 0.  Incrémenter CTR.
3. [Prochain octet.]   Si i == 16, retourner à l'étape 2.  Sinon, envoyer C[i] 
                       comme prochain octet pseudo-aléatoire, puis incrémenter i.
                       Re-effectuer l'étape 3.
'''


def aes_128_ctr(Kaes, IV, output_size):
    """
    AES-128-CTR used as a PRG
    K : AES key (bytes)
    IV : CTR IV (int)
    """
    CTR = IV
    a = AES(Kaes)
    P = CTR.to_bytes(16, 'big')
    C = a.encrypt(P)
    i = 0
    CTR += 1

    res = ''
    count = 0
    while count < output_size:
        if i == 16:
            P = CTR.to_bytes(16, 'big')
            C = a.encrypt(P)
            i = 0
            CTR += 1
        else:
            res += hex(C[i]).lstrip('0x').zfill(2)
            i += 1
            count += 1
    # print('CTR : ', CTR)
    return res


def cipher_counter_encrypt(cle, vector, data):
    K = base64.b16decode(cle, casefold=True)
    IV = vector
    data = data.encode().hex()
    key = aes_128_ctr(K, IV, len(data) // 2)
    i = 0
    cipher = ''
    while i < len(data):
        t1 = int(data[i:i + 2], 16)
        t2 = int(key[i:i + 2], 16)
        C = hex(t1 ^ t2)[2:].zfill(2)
        cipher += C
        i += 2
    return cipher


data = "Les sanglots longs\nDes violons\nDe l'automne\nBlessent mon coeur\nD'une langueur\nMonotone."
cipher = cipher_counter_encrypt("00000000000000000000000000000000", 0, data)
result = "2a8c38f49ceb425ce4238e2aea5844403f91f68a9f0d10175f107138ca944f1e66a8b6e901c3d7fd9e46a7b333de9b0b84f0" \
         "c4df6926364dd79ee69ae1f9cba407777f446e1ff5b447fcd3d9a299e68fa722d6767feb07"
print(cipher)
