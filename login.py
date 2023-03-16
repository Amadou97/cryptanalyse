import re
import pexpect
import subprocess
import os

USER = 'amadou.bayo'
PATH_CLIENT = 'python3 ./telnet_client.py'  # Change this
PATH_TELNET = 'telnet crypta.sfpn.net'
MY_PRIV_KEY = './private.key'

# checkpoint
DIGICODE = True
SAS_SERVEUR = True
DISTRIBUTEUR = True
BAKA = True

# stuff
WALKMAN = True
ECRAN = True and DIGICODE  # Nécessite DIGICODE
USB_BQ = True
PIED_DE_BICHE = True
OUTIL_RFID = True
CHARGEUR = True and DISTRIBUTEUR  # Nécessite DISTRIBUTEUR
UPLOADER = True and BAKA  # Nécessite BAKA


class Login:
    def __init__(self, client=True):
        self.client = client
        self.child = None
        self.login(client)

    def interact(self):
        self.child.interact()

    def login(self, client=True):
        if client:
            self.spawn_client()
        else:
            self.spawn_telnet()
        self.goto_automate()
        self.automate_login()
        self.equip_stuff()
        self.exit_zamanski()
        self.find_stuff()

    ### LOGIN ###

    def spawn_client(self):
        self.child = pexpect.spawn(PATH_CLIENT)
        self.child.expect('>>>')
        self.child.sendline('ascenseur')
        self.child.expect('Press any key')
        self.child.sendline()

    def spawn_telnet(self):
        self.child = pexpect.spawn(PATH_TELNET)
        self.child.expect('So, what do you have to say:')
        self.child.sendline('crypto')
        self.child.expect('>>>')
        self.child.sendline('n')

    def goto_automate(self):
        self.child.expect('>>>')
        self.child.sendline('local technique')
        self.child.expect('>>>')
        self.child.sendline('automate de service')

    def select_login(self):
        self.child.expect('\*\*\*')
        self.child.sendline('1')
        self.child.expect('Username:')
        self.child.sendline(USER)

    def sign_login(self):
        self.child.expect('Signature:')
        console = self.child.before.decode('utf-8')
        begin = console.find('31m') + 3
        end = console[begin:].find('\x1b')
        message = console[begin:begin + end]
        signature = sign(message, MY_PRIV_KEY)
        self.child.sendline(signature)
        self.child.expect('Successful login. Press any key.')
        self.child.sendline('')

    def pick_badge(self):
        self.child.expect('\*\*\*')
        self.child.sendline('3')
        self.child.expect('Badge delivery successful. Press any key.')
        self.child.sendline('')

    def automate_login(self):
        self.select_login()
        self.sign_login()

        if DIGICODE or DISTRIBUTEUR:
            self.child.expect('Press any key')
            self.child.sendline('')

        self.pick_badge()

        self.child.expect('\*\*\*')
        self.child.sendline('Q')

    def equip_stuff(self):
        if DIGICODE:
            self.child.expect('>>>')
            self.child.sendline('prendre downloader')
        if SAS_SERVEUR:
            self.child.expect('>>>')
            self.child.sendline('carte micro-SD')
        if CHARGEUR:
            self.child.expect('>>>')
            self.child.sendline('prendre chargeur')
        if UPLOADER:
            self.child.expect('>>>')
            self.child.sendline('take uploader')
            self.child.expect('>>>')
            self.child.sendline('take une carte électronique suspecte')
            self.child.expect('>>>')
            self.child.sendline('take un lecteur de DIMM')
            if CHARGEUR:
                self.child.expect('>>>')
                self.child.sendline('utiliser chargeur')

    def exit_zamanski(self):
        self.child.expect('>>>')
        self.child.sendline('s')
        self.child.expect('Ici se trouve un ascenseur de service.')
        self.child.sendline('bouton')
        self.child.expect('Press any key.')
        self.child.sendline('')
        self.child.expect('>>>')
        self.child.sendline('hall')
        self.child.expect('>>>')
        self.child.send('porte\n')

    ## FAC ###

    def mir(self):
        self.child.expect('>>>')
        self.child.sendline('tour 25')
        self.child.expect('>>>')
        self.child.sendline('mir')
        self.child.expect('>>>')
        self.child.sendline('mir')

    def eve(self):
        self.child.expect('>>>')
        self.child.sendline('tour 25')
        self.child.expect('>>>')
        self.child.sendline('tour 24')
        self.child.expect('>>>')
        self.child.sendline('eve')
        self.child.expect('>>>')
        self.child.sendline('entrer')

    def amphi(self):
        self.child.expect('>>>')
        self.child.sendline('tour 25')
        self.child.expect('>>>')
        self.child.sendline('amphi')

    def tour(self, num):
        path = [26, 25, 24, 14, 15]
        if num not in path:
            raise ValueError('Tour inconnue')

        while True:
            self.child.expect('>>>')
            self.child.sendline('tour {}'.format(path[0]))
            if path.pop(0) == num:
                self.child.expect('>>>')
                break

    def etage(self, num):
        max_etage = 'Impossible depuis cet endroit'
        self.child.sendline('monter')
        self.child.expect('>>>')
        console = self.child.before.decode('utf-8')
        texte = '1er étage' if num == 1 else '{}ème étage'.format(num)
        while not max_etage in console and not texte in console:
            self.child.sendline('monter')
            self.child.expect('>>>')
            console = self.child.before.decode('utf-8')

    ### STUFF ###

    def find_pied_de_biche(self):
        self.etage(1)
        self.child.sendline('tour 25')
        self.child.expect('>>>')
        self.child.sendline('prendre pied-de-biche')
        self.child.expect('>>>')
        self.child.sendline('tour 26')
        self.child.expect('>>>')
        self.child.sendline('down')

    def find_usb_bq(self):
        self.etage(2)
        self.child.sendline('lip6')
        self.child.expect('>>>')
        self.child.sendline('distributeur')
        self.child.expect('\$\$\$')
        console = self.child.before.decode('utf-8')
        begin = console.find('Cable USB-BQ') - 5
        end = begin + 2
        self.child.sendline(console[begin:end])
        self.child.expect("machine.")
        self.child.sendline('')
        self.child.expect('>>>')
        self.child.sendline('prendre usb-bq')
        self.child.expect('>>>')
        self.child.sendline('sortir')
        self.child.expect('>>>')
        self.child.sendline('down')
        self.child.expect('>>>')
        self.child.sendline('down')

    def find_walkman(self):
        self.child.expect('>>>')
        self.child.sendline('amphi')
        self.child.expect('>>>')
        self.child.sendline('prendre walkman')
        self.child.expect('>>>')
        self.child.sendline('monter')

    def find_outil_rfid(self):
        self.child.expect('>>>')
        self.etage(3)
        self.child.sendline('tour 25')
        self.child.expect('>>>')
        self.child.sendline('salle sesi')
        self.child.expect('>>>')
        self.child.sendline('prendre outil')
        self.child.expect('>>>')
        self.child.sendline('sortir')
        self.child.expect('>>>')
        self.child.sendline('tour 24')
        self.child.expect('>>>')
        self.child.sendline('down')
        self.child.expect('>>>')
        self.child.sendline('down')

    def find_ecran(self):
        self.child.expect('>>>')
        self.child.sendline('up')
        self.child.expect('>>>')
        self.child.sendline('tour 15')
        self.child.expect('>>>')
        self.child.sendline('salle serveur')
        self.child.expect('>>>')
        self.child.sendline('utiliser ecran')
        self.child.expect('>>>')
        self.child.sendline('sortir')
        self.child.expect('>>>')
        self.child.sendline('tour 14')
        self.child.expect('>>>')
        self.child.sendline('down')

    def find_stuff(self):
        self.child.expect('>>>')
        self.child.sendline('tour 26')

        if PIED_DE_BICHE:
            self.find_pied_de_biche()

        if USB_BQ:
            self.find_usb_bq()

        self.child.expect('>>>')
        self.child.sendline('tour 25')

        if WALKMAN:
            self.find_walkman()

        self.child.expect('>>>')
        self.child.sendline('tour 24')

        if OUTIL_RFID:
            self.find_outil_rfid()

        self.child.expect('>>>')
        self.child.sendline('tour 14')

        if ECRAN:
            self.find_ecran()

        self.child.expect('>>>')
        self.child.sendline('tour 24')
        self.child.expect('>>>')
        self.child.sendline('tour 25')
        self.child.expect('>>>')
        self.child.sendline('tour 26')
        self.child.expect('>>>')
        self.child.sendline('tour Zamanski')

    def goto(self, path):
        if path == 'mir':
            return self.mir()
        elif path == 'eve':
            return self.eve()
        elif path == 'amphi':
            return self.amphi()
        elif path == 'yanny' or path == 'secretariat':
            return self.goto('24-25/2')
        elif path == 'ppti':
            return self.goto('14-15/4')
        elif path == 'ppti1':
            return self.goto('14-15/5')
        else:
            tour = re.search(r'(\d+)', path)
            tour_etage = re.search(r'(\d+)\/(\d+)', path)
            couloir = re.search(r'(\d+)-(\d+)\/(\d+)', path)

            if couloir:
                t1, t2, etage = int(couloir.group(1)), int(couloir.group(2)), int(couloir.group(3))
                self.tour(t1)
                self.etage(etage)
                if t1 == 26 and t2 == 0:
                    t = '00' if etage == 3 else 'LIP6'
                else:
                    t = str(t2)

                self.child.sendline(t)
            elif tour_etage:
                tour, etage = int(tour_etage.group(1)), int(tour_etage.group(2))
                self.tour(tour)
                self.etage(etage)
                print(self.child.before.decode('utf-8'))
                print('>>>', end=' ')
            elif tour:
                self.tour(int(tour.group(0)))
                print(self.child.before.decode('utf-8'))
                print('>>>', end=' ')
            else:
                raise ValueError('Lieu inconnu')


### ANNEXE ###
def write_temp_file(content, ext=''):
    """
    Writes content in a temporary file and returns its name
    """
    i = 0
    while os.path.isfile('tmp' + str(i)):
        i += 1
    file = 'tmp' + str(i)
    if ext and ext[0] != '.':
        ext = '.' + ext
    file += ext
    with open(file, 'w') as f:
        os.system("attrib +h " + file)
        f.write(content)
    return file


def sign(file, key, algorithm='sha256'):
    """
    Signs a file/message with a private key
    """
    args = ['openssl', 'dgst']
    args.extend(['-{}'.format(algorithm)])
    args.extend(['-hex'])
    args.extend(['-keyform', 'PEM'])

    # key
    if not os.path.isfile(key):
        raise ValueError('File not found / Invalid key')
    args.extend(['-sign', key])

    # message
    message = not os.path.isfile(file)
    if message:
        file = write_temp_file(file, '.txt')
    args.extend([file])

    # execute
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # free
    if message:
        os.remove(file)

    # output
    result = result.stdout.decode('utf-8')
    return result[result.find('=') + 2:]
