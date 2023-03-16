#  Il faut en fait mettre en oeuvre une attaque classique contre le chiffrement RSA
#  ``textbook'' (c'est-à-dire sans bourrage) qui exploite la malléabilité du
#  chiffrement.  Avec probabilité environ 20%, le nombre K de 48 bits peut s'écrire
#  comme K = A*B, où les deux entiers A et B font 24 bits chacun.  Le chiffré de K
#  est le produit des chiffrés de A et B (modulo N bien sûr).
#
#  Du coup, on peut mettre en oeuvre la stratégie suivante, qui est un compromis
#  temps-mémoire permettant de réaliser le déchiffrement de c (en fait c'est une.
#  variante de l'algorithme ``Baby Steps / Giants Steps'').
#
#  1. [Initialisation] Initialiser un dictionnaire D (vide).
#  2. [Construction]   Pour chaque 1 <= i < 2**24 :
#                        Calculer x <-- i**e % N puis stocker D[x] <-- i.
#  3. [Recherche]      Pour chaque 0 <= j < 2**24 :
#                        Calculer x <-- j**e % N et y <-- c * x**(-1) % N.
#                        Si y est une clef du dictionnaire D:
#                            Poser i <--- D[y].  On a alors c == (i * j)**e % N.
import hmac
import hashlib
from gmpy2 import powmod
"""
c = 0x0136e4b95fbdeb4da90bafb3dd8122892bfcf9deda08413dff36170083ef9f25ccc196579a12a5aa4ccd4338cd1d77608576f69a7bdc58f33c1887b8add036c9bb3b9589b0c38a32fe57c89963471a8da9163fb8ef5a753f65dafddf7410f920006a02ba57bddea32bdf805726ee4ef875335ef744391a5a6bd9398031b91af9
e = 0x10001
N = 0x1ea982ba8f01d5e03163b0409a554484b8e145af768a8d3e66b84c9723d8604a33bd7c52033def81adfaf49beaa4f0f2b3b92370efb88f07665c5c35afdfd94752eacc4cf24ff3b96954ff391abaf39108df0cf11c26567ac2aa408143038ed11d53172667b95637a7cd3d6bc8972e6a4d7a503730db2af935d3baf8d5a5465d
"""
e = 97
N = 4097
c = (59 * 23)**e % N

memo = {}
oui = False

for i in range(1, 2**24):
    x = pow(i, e, N)
    memo[x] = i
print("youpi")

for j in range(1, 2**24):
    x = powmod(j, e, N)
    y = c * powmod(x, -1, N)

    if y in memo:
        i = memo[y]
        oui = i * j
        print(oui)
        print(oui**e % N)
        print(c)
        break

if oui:
    hsh = hmac.new(oui.to_bytes(6, 'big'), 0x00000000.to_bytes(4, 'big'), hashlib.sha256)
    print('00000000' + hsh.hexdigest())
else:
    print("Try again")
