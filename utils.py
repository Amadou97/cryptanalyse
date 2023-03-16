import subprocess
import os
from datetime import datetime,timezone,timedelta

def nth_root(x, n):
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1

def read_ppti_pk(key):
    args = ['openssl', 'rsa', '-pubin', '-inform', 'PEM' ,'-text', '-noout']

    args.append('-modulus')

    # key
    if not os.path.isfile(key):
        raise ValueError('File not found')
    args.extend(['-in', key])

    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')
    # extract modulus and exponent
    s = result[result.find('Exponent: ')+len('Exponent: '):]
    e = s[:s.find(' (0x')]
    n = result[result.find('Modulus=')+8:]

    # Format values
    e = int(e)
    n = int(n,16)
    return n,e

def auto_date(offset=0):
    date = (datetime.now(timezone.utc) + timedelta(minutes=offset)).strftime('%Y-%m-%d %H:%M UTC')
    plaintext = f'PPTI SERVER ACCESS ON {date}'
    return plaintext.encode()