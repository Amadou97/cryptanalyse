from twisted.protocols.basic import NetstringReceiver
from Crypto.Util import Counter
from Crypto.Cipher import AES
import base64
import hmac
import hashlib
from random import randint
import json
import os

# Paramètre serveur :
param_server = """-----BEGIN X9.42 DH PARAMETERS-----
    MIICLAKCAQEAh6jmHbS2Zjz/u9GcZRlZmYzu9ghmDdDyXSzu1ENeOwDgDfjx1hlX
    1Pr330VhsqowFsPZETQJb6o79Cltgw6afCCeDGSXUXq9WoqdMGvPZ+2R+eZyW0dY
    wCLgse9Cdb97bFv8EdRfkIi5QfVOseWbuLw5oL8SMH9cT9twxYGyP3a2Osrhyqa3
    kC1SUmc1SIoO8TxtmlG/pKs62DR3llJNjvahZ7WkGCXZZ+FE5RQFZCUcysuD5rSG
    9rPKP3lxUGAmwLhX9omWKFbe1AEKvQvmIcOjlgpU5xDDdfJjddcBQQOktUMwwZiv
    EmEW0iduEXFfaTh3+tfvCcrbCUrpHhoVlwKCAQA/syybcxNNCy53UGZg7b1ITKex
    jyHvIFQH9Hk6GguhJRDbwVB3vkY//0/tSqwLtVW+OmwbDGtHsbw3c79+jG9ikBIo
    +MKMuxilWuMTQQAKZQGW+THHelfy3fRj5ensFEt3feYqqrioYorDdtKC1u04ZOZ5
    gkKOvIMdFDSPby+Rk7UEWvJ2cWTh38lnwfs/LlWkvRv/6DucgNBSuYXRguoK2yo7
    cxPT/hTISEseBSWIubfSu9LfAWGZ7NBuFVfNCRWzNTu7ZODsN3/QKDcN+StSx4kU
    KM3GfrYYS1I9HbJGwy9jB4SQ8A741kfRSNR5VFFeIyfP75jFgmZLTA9sxBZZAiEA
    jPg2QqcJoJe0R5l2QBKdopmxpH0es3ULowiw/mT1+9M=
    -----END X9.42 DH PARAMETERS-----"""
# openssl asn1parse < param_serveur
p = 0x87A8E61DB4B6663CFFBBD19C651959998CEEF608660DD0F25D2CEED4435E3B00E00DF8F1D61957D4FAF7DF4561B2AA3016C3D91134096FAA3BF4296D830E9A7C209E0C6497517ABD5A8A9D306BCF67ED91F9E6725B4758C022E0B1EF4275BF7B6C5BFC11D45F9088B941F54EB1E59BB8BC39A0BF12307F5C4FDB70C581B23F76B63ACAE1CAA6B7902D52526735488A0EF13C6D9A51BFA4AB3AD8347796524D8EF6A167B5A41825D967E144E5140564251CCACB83E6B486F6B3CA3F7971506026C0B857F689962856DED4010ABD0BE621C3A3960A54E710C375F26375D7014103A4B54330C198AF126116D2276E11715F693877FAD7EF09CADB094AE91E1A1597
g = 0x3FB32C9B73134D0B2E77506660EDBD484CA7B18F21EF205407F4793A1A0BA12510DBC15077BE463FFF4FED4AAC0BB555BE3A6C1B0C6B47B1BC3773BF7E8C6F62901228F8C28CBB18A55AE31341000A650196F931C77A57F2DDF463E5E9EC144B777DE62AAAB8A8628AC376D282D6ED3864E67982428EBC831D14348F6F2F9193B5045AF2767164E1DFC967C1FB3F2E55A4BD1BFFE83B9C80D052B985D182EA0ADB2A3B7313D3FE14C8484B1E052588B9B7D2BBD2DF016199ECD06E1557CD0915B3353BBB64E0EC377FD028370DF92B52C7891428CDC67EB6184B523D1DB246C32F63078490F00EF8D647D148D47954515E2327CFEF98C582664B4C0F6CC41659
q = 0x8CF83642A709A097B447997640129DA299B1A47D1EB3750BA308B0FE64F5FBD3

pk_server = """-----BEGIN PUBLIC KEY-----
    MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEMM6kpDWtZnIQauXmCZdg90zLbQt/MLNU
    3158zCQrRxs3MOZF+1nZN6MIM0sZvMs6z9lTbLoTZQyw4QFC6sv3Dg==
    -----END PUBLIC KEY-----"""

sk_client = """-----BEGIN EC PRIVATE KEY-----
MFECAQEEFQAhcuHJsfB6+DPlkReg3D6wYuhJT6AHBgVnKwEEB6EsAyoABETeuKBm
rz5bIBWRINiK0OFFpzLQ/hqLPGpHrpZfMgY5nHHKybu72WE=
-----END EC PRIVATE KEY-----
"""

# Génération des clés serveur/client
Kaes_client = base64.b16decode("00000000000000000000000000000000")
Kmac_client = base64.b16decode("00000000000000000000000000000000")
Kaes_serveur = base64.b16decode("00000000000000000000000000000000")
Kmac_serveur = base64.b16decode("00000000000000000000000000000000")
Kiv_client = Counter.new(128, initial_value=0)
Kiv_serveur = Counter.new(128, initial_value=0)
cipher_serveur = AES.new(Kaes_serveur, AES.MODE_CTR, counter=Kiv_serveur)
cipher_client = AES.new(Kaes_client, AES.MODE_CTR, counter=Kiv_client)
exchange_server = True
exchange_client = True
K = 0
x = randint(0, q)
A = pow(g, x, p)


class ProtocolTransportMixin:
    """
    Act both as a protocol (w.r.t the outside world) AND a transport.
    """

    def __init__(self, protocolFactory, *args, **kwds):
        self.inner_protocol_factory = protocolFactory
        self.inner_protocol_args = args
        self.inner_protocol_kwds = kwds
        super().__init__()

    def _connect_inner_protocol(self):
        """ 
        Connects the inner protocol. Give it "self" as transport. 
        """
        # build the inner protocol from the factory 
        self.inner_protocol = self.inner_protocol_factory(*self.inner_protocol_args, **self.inner_protocol_kwds)

        # I'm the transport for the inner protocol 
        inner_transport = self
        self.inner_protocol.makeConnection(inner_transport)

    def connectionMade(self):
        """ 
        I've been started up. Start the inner protocol. 
        """
        super().connectionMade()  # make connection in potential super-class
        self._connect_inner_protocol()

        # there is no dataReceived method: subclasses have to implement it

    def connectionLost(self, reason):
        """ 
        I've lost the connection to the outside world. Notify the inner protocol. 
        """
        super().connectionLost(reason)  # lose connection in potential super-class
        self.inner_protocol.connectionLost(reason)  # lose connection in inner protocol

    # ### now the transport part.
    def write(self, data):
        """ 
        Invoked by the inner protocol when it wants to send <data> to the outside world.  
        Intercept outgoing data, process, send to my own ("external") transport. 
        """
        self.transport.write(data)

    def writeSequence(self, seq):
        self.write(b''.join(seq))

    def loseConnection(self):
        """ 
        Inner protocol wants to abort. We abort. 
        """
        self.transport.loseConnection()

    def getHost(self):
        """ 
        Inner protocol asks about the connected party. We forward the query... 
        """
        return self.transport.getHost()

    def getPeer(self):
        return self.transport.getPeer()


class NetstringWrapperProtocol(ProtocolTransportMixin, NetstringReceiver):
    """ 
    This protocol receives netstrings. When a complete netstring is received, 
    the payload is sent to the inner protocol. When the inner protocol sends 
    bytes, they are wrapped inside a netstring and sent to the outside world. 

    IMPLEMENTATION DETAILS : 

    The connectionMade() method is inherited from ProtocolTransportMixin (both 
    parent classes implement this method, but we inherit from 
    ProtocolTransportMixin first, so it wins). It starts the inner proto AND 
    call super().connectionMade(), which will resolve to 
    NetstringReceiver.connectionMade()... 

    The dataReceived() method is inherited from NetstringReceiver, because 
    ProtocolTransportMixin does not implement it. It will call the 
    stringReceived() method of this class once a netstring is received. 
    """

    def stringReceived(self, data):
        """ 
        netstring received and decoded. Forward to inner proto. 
        """
        global exchange_server
        global Kaes_client, Kaes_serveur
        global Kmac_client, Kmac_serveur
        global cipher_client, cipher_serveur
        global K

        # Echange de clef diffie-hellman
        if exchange_server == False:
            # print(data)
            # Mise à jour de exchange
            exchange_server = True

            # Récupère le JSON envoyer par le serveur
            J = json.loads(data)

            # On récupère la signature pour le vérifier
            signature = J["signature"]
            S = str(A) + "," + str(J["B"]) + "," + "amadou.bayo"
            print(S, signature)
            fic = open("S.txt", "w")
            fic.write(S)
            fic.close()

            # On transforme la signature sous format binaire
            fic = open("sign_server.sign", "w")
            fic.write(signature)
            fic.close()
            os.system("(cat sign_server.sign)|(xxd -r -p)> binary_sign.sign")
            # Vérification signature serveur
            res = os.system("openssl dgst -sha256 -verify ./clefs/public-key_server.pem -signature binary_sign.sign "
                            "S.txt")

            if res == 0:
                # Calcul de K et des clés
                K = pow(J["B"], x, p)
                A_kaes = str(K) + "A"
                B_kiv = str(K) + "B"
                C_Kmac = str(K) + "C"
                Kaes_serveur = hashlib.sha256(A_kaes.encode()).digest()[:16]
                tmp = int(hashlib.sha256(B_kiv.encode()).digest()[:16].hex(), 16)
                Kiv_serveur = Counter.new(128, initial_value=tmp)
                Kmac_serveur = hashlib.sha256(C_Kmac.encode()).digest()[:16]
                cipher_serveur = AES.new(Kaes_serveur, AES.MODE_CTR, counter=Kiv_serveur)

                # Calcul client
                D_kaes = str(K) + "D"
                E_kiv = str(K) + "E"
                F_Kmac = str(K) + "F"
                Kaes_client = hashlib.sha256(D_kaes.encode()).digest()[:16]
                tmp = int(hashlib.sha256(E_kiv.encode()).digest()[:16].hex(), 16)
                Kiv_client = Counter.new(128, initial_value=tmp)
                Kmac_client = hashlib.sha256(F_Kmac.encode()).digest()[:16]
                cipher_client = AES.new(Kaes_client, AES.MODE_CTR, counter=Kiv_client)

        # print("data received : {0}".format(data))
        else:
            l = len(data)
            decrypt_data = data[:l - 32]
            tag = data[l - 32:]

            ct = cipher_serveur.decrypt(decrypt_data)
            # Vérification du tag
            verify = hmac.new(Kmac_serveur, ct, hashlib.sha256).digest()
            if tag == verify:
                # print("data ct received : {0}".format(ct))
                self.inner_protocol.dataReceived(ct)

    def write(self, data):
        """ 
        Intercept outgoing data from inner protocol, wrap in netstring and 
        send to external transport. 
        """
        global exchange_client, exchange_server

        # déchiffrement
        if exchange_client == True and exchange_server == True:

            # print("data write : {0}".format(data))
            ct = cipher_client.encrypt(data)
            # print("data ct write : {0}".format(ct))
            tag = hmac.new(Kmac_client, data, hashlib.sha256).digest()
            # print("data tag write : {0}".format(tag))
            aut_data = ct + tag
            # print("data aut_data : {0}".format(aut_data))
            self.sendString(aut_data)  # inherited from NetstringReceiver

        # Echange de clé diffie-hellman

        elif exchange_client == False:

            # Mise à jour de exchange
            exchange_client = True

            # Génération des messages
            A_str = str(A)

            # Signature de A
            fic = open("sign_A", "w")
            fic.write(A_str)
            fic.close()
            os.system("openssl dgst -sha256 -hex -sign ./clefs/private-key.pem -out sign_A.txt.sign sign_A")
            # Récupération signature
            fic = open("sign_A.txt.sign", "r")
            r = fic.readlines()
            fic.close()
            res = r[0]

            # Création du JSON
            D = dict()
            D["username"] = "amadou.bayo"
            D["A"] = A
            D["signature"] = res[19:len(res) - 1]
            J = json.dumps(D)
            print(J.encode('utf-8'))
            self.sendString(J.encode('utf-8'))
