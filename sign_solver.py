from pkcs1 import *
from utils import *

def format_message(plaintext):
    HEADER = '0001'
    PADDING = 'ff' * 10
    message = HEADER + PADDING + '00' + HASH_ID.hex() + sha256(plaintext).hexdigest()
    garbage = '7' * (512 - len(message))
    message = int(message + garbage, 16)
    return message


def sign(message):
    k = key_length(n)
    sign = nth_root(message, 3)
    sign = i2osp(sign, k)
    return sign.hex()


######################

PPTI_PK = 'ppti_pk.pem'
n, e = read_ppti_pk(PPTI_PK)

plaintext = auto_date(offset=0)
# plaintext = b"PPTI SERVER ACCESS ON 2022-10-17 20:20 UTC"

message = format_message(plaintext)
signature = sign(message)

assert rsa_pkcs_verify(n, 3, plaintext, bytearray.fromhex(signature))

print('date=', plaintext.decode())
print('id= ppti_server_room')
print('sign=', signature)