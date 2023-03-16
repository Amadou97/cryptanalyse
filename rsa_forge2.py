from binascii import hexlify, unhexlify
from datetime import datetime, timedelta
from hashlib import sha256
from decimal import Decimal, getcontext

HASH_ID = b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20'
keysize = 2048


def toInt(val):
    return int(hexlify(val), 16)


def toBytes(val):
    hexVal = hex(val)[2:-1]
    if len(hexVal) % 2 == 1:
        hexVal = "0" + hexVal
    return unhexlify(hexVal)


def nthroot(n, A, precision=300):
    getcontext().prec = precision

    n = Decimal(n)
    x_0 = A / n
    x_1 = 1
    while True:

        x_0, x_1 = x_1, (1 / n) * ((n - 1) * x_0 + (A / (x_0 ** (n - 1))))
        if x_0 == x_1:
            return x_1


def encodePkcs1Suffix(message):
    messageHash = sha256(message.encode()).digest()
    if messageHash[-1] & 0x01 == 0x01:
        suffix = b"\x00" + HASH_ID + messageHash
        return suffix
    else:
        print("Hash value is not even for: ", message)
        return b"NOT EVEN"


def forge_signature(message, psLength=8):
    prefix = b"\x00\x01"
    prefix += b"\xFF" * psLength
    suffix = encodePkcs1Suffix(message)
    if suffix == b"NOT EVEN":
        return suffix
    plain = prefix + suffix + b"\x00" * ((keysize // 8) - (len(prefix) + len(suffix)))
    signature = toBytes(int(nthroot(3, toInt(plain))) + 1)
    return hexlify(signature)


if __name__ == '__main__':
    current_utc = datetime.utcnow()
    i = 3
    while True:
        next_utc = current_utc + timedelta(minutes=i)
        s = str(next_utc)
        message = "PPTI SERVER ACCESS ON " + s[:s.rindex(':')] + ' UTC'
        signature = forge_signature(message).decode()
        if signature != "NOT EVEN":
            break
        else:
            i += 1

    padding = "0" * (516 - len(signature))
    signature = padding + signature
    print("Forged signature for '{}' : {}".format(message, signature))