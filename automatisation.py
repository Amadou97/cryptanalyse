import pexpect
import os

HOST = "crypta.sfpn.net"
USER = "amadou.bayo"
Pk_file = "public.pem"
Pvk = "private.key"


# Create the signature of the challenge in filename
def create_sign(filename):
    a = "challenge"
    sign_file = "signature-" + a  # filename
    cmd = "openssl dgst -sign " + Pvk + " -hex -out " + sign_file + " " + a  # filename
    os.system(cmd)
    return sign_file


# Return the signature in filename
def read_sign(filename):
    with open(filename, 'r') as file:
        data = file.read()
    data = data.replace("EC-SHA256(challenge)= ", "")
    data = data.replace("\n", "")
    return data


def get_badge(child):
    child.expect('So, what do you have to say:')
    child.sendline("crypto")
    child.expect(">>>")
    child.sendline("sortir")
    child.expect(">>>")
    child.sendline("local technique")
    child.expect(">>>")
    child.sendline("automate de service")
    child.sendline("1")
    child.expect("Username:")
    child.sendline(USER)

    # Signature
    child.expect("Signature:")
    chall = child.before.decode("UTF-8")
    chall = chall[chall.find(':') + 14:]
    test = chall.split('\r')
    chall = test[0]
    chall = chall[:chall.find('\x1b')]

    # Write the challenge in a file
    filename = "challenge"
    with open(filename, 'w') as file:
        file.write(chall)

    sign_file = create_sign(filename)
    signature = read_sign(sign_file)
    child.sendline(signature)

    child.expect("key")
    child.sendline("3")
    child.sendline("3")

    child.expect("key")
    child.sendline("3")
    # child.expect("key.")
    child.sendline("Q")
    child.expect("Q")

    # take all
    child.sendline("take downloader")
    child.sendline("take uploader")
    child.sendline("take carte micro-SD")
    child.sendline("take chargeur universel")
    child.sendline("take carte électronique suspecte")
    child.sendline("take lecteur de DIMM")


# Connect to the server
child = pexpect.spawn("telnet", [HOST])
get_badge(child)
child.sendline("sortir")
child.expect(">>>")
child.sendline("utiliser badge")
child.expect("key.")
child.send("d")
child.expect(">>>")
child.sendline("portillon")
"""
child.expect(">>>")
child.sendline("sortir")
child.sendline("tour 26")
child.expect(">>>")
child.sendline("tour 15")
child.expect(">>>")
child.sendline("monter")
child.expect(">>>")
child.sendline("tour 25")
"""
# print("child interact")

child.sendline("une carte électronique suspecte")
child.expect("Single/Batch :")
child.sendline("Batch")
child.expect("Encryption/Decryption :")
child.sendline("Encryption")
child.expect(">>>")
value = "be2dc337414574062aeedbfa21b5af13"
child.sendline(value)
child.expect(">>>")
child.sendline("\n")
child.expect("OUTPUT")
child.expect("-----BEGIN OUTPUT-----")
cipher = child.before.decode("UTF-8")
cipher = cipher[cipher.find(':') + 32:]
#test = cipher.split('\r')
#cipher = test[0]
#cipher = cipher[:cipher.find('\x1b')]


child.interact()
