#!/usr/bin/env python
import Utils
import gmpy
import sys

sys.path.append('PATH_TO_TENSORFLOW_OBJECT_DETECTION_FOLDER')

class Hastad(object):
    '''
    Hastad Broadcast Attack
    '''

    def __init__(self):
        '''
        ns: array of n
        e: public exponent
        cs: array of cipher text
        '''

        n1 = 24024333509900754918918504952116864975126125908311896546098801562440649260224244924351392952815987412539261304682378039271110969398655318946507124857780930710329615794046877426969291480224417538230325888861393214705080648578689861908126043868642461236961583491866880865761079394964058246109597431684290825813193992881531532072488237528304547965063476937207772865729773049024783806601295872275143972309276670822440167716502616883175980070939465062525691685962307213337779283331387666346762424613174122880909563440958037380724965090866562638620374044216788329974541289723966093642151260357738139302203870759529650688347
        n2 = 29377846774702184198925337039846334967067434261326607063416333980076595357031915025484834679220426609187984616215117407932712771976538758362547715478082335643088055664104356185793722117883931231652242368163396502413939236966011896776177199396691807851620973762062992157832889592077183593149922606298365414037520430986386012235916068875801683775560076008767425186985301012891027953700303954454130092092605240172817473022414968293315681008366672647768253951766061204233676947008306451713060755555936813725958452874358543368757030876828141145083895402174081124937468858034662998456480030621597201107597693670108691980707
        n3 = 23577587684046707966380295377115733071785721606403699058865286187113812638568836764075088643042718056260174536775846420350859378445094951940589402178355491232723979774647149984763258617231669388345954709555720488933332112874271678178068927487155975168187380486613264602922858167887834496348069911573142748474376508949166038624594576799534861530225838503427247145953198245469410858990147401142758446420834461230834672254870222021724850602608691631284878054711676477214108874520310043640922085788981007002174689325948187082062194282509703310926773635381426433940450744848916759607238239748168232733532363556001560001517



        c1 = "63b8605601fccb0b8e53aff0f49f931fdae6f7feab350b96bde98971d3227a38d47361f872aaf34eceaa4dd5df90bd6bc0e87c2b92ee7c808eb7bc7ffbfca2f27783cd68ff659fefd547e460758a30c1cea00b41d29b8d930a6194238d13e62726f36726aa73a844606764476cd9729b05c06ac379525ca2f1c10971132ab0ccdc106f6ebbae92f75ff367f05ebcb54491d3240a891e36ebec2651864b3130fc0c7124c83a1511ceedca77284eb4bad156526e5804863ef3323d549fd4ad1ab97095f8755d6f2619aafe7285e10542f822252596da7ae21c764cafdf90f8ce4abc280396908a07e644bdf5091ee97d4c763e5b6eaad68fc35447cd6d033f8a52"
        c2 = "19d90b9e5ed2d78f47d6291fd42e6c4648ace0142f42e1552b9e2bda422075d535a0d28b4c323ea4619c77915ad3e4f42dab220d5658c9bb3c09d68fa25a79e01c02e28cf38738c1328997af848e8db0c459c4a95a8b09ebcb70b408f1c68694143540496f8fd6680237f0bff054832f8e8908efbbe2d9611fa2009e5ca54858dd9081124d6f12a00c980b9de632561ef24ee44ca9cab711b4040b402a40d243da01efcc0713e1759a51565cbc6e9e483526681308993e378b272e293c21b474c3f5a904b6c4dcd843c996730656e729553fd8384614ffc677f1b176e1194ccb82769e759e2be68e2ccbc693e8ecbac823bc490c0c29f7df4b54204f955b6384"
        c3 = "32d71f5796d9fc3a42b1e1095470c007971ffd3ca3d6514a2cfe7eef5db21c78ff503cf1245ce82efe143c4ae04c86409c93c17da54bb360de6e4e49f54f11fe7691d03381745902bc6b3b0494115c7149c45e927ccd50723a05c9dcb873655c680028a3bf8bccb404f4d8774a2b4efd44bfac66091ed113229e29b5a076794f81641e6206e21cf0c30f1ae2863e2c84fbd88b37296498ab605ffec18e7ffabab69ad05849cac1590f01d01592c78ff952f59993a063dfebd0d4114de6ea523903b29ce2ea611c2a68c29b7e4bce218e142d319d805f06971ac7d0ad9cf2eefc101ac1d2c2c239e5a8d04278fd4947c295b31c86de48da9de00f4559f56c2b92"

        self.ns = [n1, n2, n3]
        self.e = 3
        self.cs = [c1, c2, c3]

    def decrypt(self):
        s = Utils.CRT(self.ns, self.cs)
        pt, perfect = gmpy.root(s, self.e)
        if perfect:
            return pt
        else:
            print("Cannot find %dth root of %s" % (self.e, hex(s)))



h = Hastad()
print(h.decrypt())
