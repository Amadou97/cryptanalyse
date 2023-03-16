from Crypto.PublicKey import RSA
import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5  # For signature/Verify Signature
from Crypto.Cipher import PKCS1_v1_5  # For encryption
from Crypto import Random
from Crypto import Hash
import math
import hashlib


def find_invpow(x,n):
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    high = 1
    while high ** n < x:
        high *= 2
    low = high//2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1


N = 29971517447756160893726736250536905443548504813504284896984751825839546244413329684299200665188566779236583882767852278100540254036350393501530123976884805681815257684680924358973550769819862208842119186687219381975030681235034871767304259068970137000583524958045118557588775043119270030528453635333333198175965832303008987896683678362800584679621490008349470309966535082244001517345918970091849799913095883875072409621665643222671973209425100776707920983270806154154372377392006880380151227473235045375141668536529354036565744714841193551740696712512479283786563167396011266068839537902932051453392744340546892061261

msg = "PPTI SERVER ACCESS ON 2022-02-22 22:35 UTC"
msg = msg.encode()

k = math.ceil(N.bit_length() // 8) # Modulus // 8

hash_id = "3031300D060960864801650304020105000420" # HASH_ID --> bit magique qui identifie

hash = hashlib.sha256(msg).hexdigest() # sha256(M)

filler = "0001" + "FF" * 8 + "00" # au moins 10 F
junkless = filler + hash_id + hash # bourrage final

junk = (k - len(junkless) // 2) * "FF"
S3 = junkless + junk
NS3 = int(S3, 16)
NS = find_invpow(NS3, 3)
NS3p = pow(NS, 3, N)
S3p = "000" + hex(NS3p)[2:]
l = len(junkless)
assert(S3p[:l].lower() == S3[:l].lower())
Ss = hex(NS)[2:]
Ss = "00" * (k - len(Ss)//2) + Ss
Ssi = int(Ss, 16)
Ssb = Ssi.to_bytes(len(Ss)//2, 'big')

print(Ssb.hex().encode())