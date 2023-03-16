cipher = """(hex, 128 bits, 1 per line, in order): 
-----BEGIN OUTPUT-----
3452e7e6686242684ff0c248d7967387
-----END OUTPUT-----"""

#cipher = cipher[cipher.find(':') + 32:]
test = cipher.split('\n')
#cipher = test[0]
#cipher = cipher[:cipher.find('\x1b')]



print(test)
