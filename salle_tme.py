#openssl pkey  -pubin -pubout -text -in filename
import binascii
import string
import codecs
import gmpy2 as gmpy2
from gmpy2 import mpz

c1 = "63b8605601fccb0b8e53aff0f49f931fdae6f7feab350b96bde98971d3227a38d47361f872aaf34eceaa4dd5df90bd6bc0e87c2b92ee7c808eb7bc7ffbfca2f27783cd68ff659fefd547e460758a30c1cea00b41d29b8d930a6194238d13e62726f36726aa73a844606764476cd9729b05c06ac379525ca2f1c10971132ab0ccdc106f6ebbae92f75ff367f05ebcb54491d3240a891e36ebec2651864b3130fc0c7124c83a1511ceedca77284eb4bad156526e5804863ef3323d549fd4ad1ab97095f8755d6f2619aafe7285e10542f822252596da7ae21c764cafdf90f8ce4abc280396908a07e644bdf5091ee97d4c763e5b6eaad68fc35447cd6d033f8a52"
c2 = "19d90b9e5ed2d78f47d6291fd42e6c4648ace0142f42e1552b9e2bda422075d535a0d28b4c323ea4619c77915ad3e4f42dab220d5658c9bb3c09d68fa25a79e01c02e28cf38738c1328997af848e8db0c459c4a95a8b09ebcb70b408f1c68694143540496f8fd6680237f0bff054832f8e8908efbbe2d9611fa2009e5ca54858dd9081124d6f12a00c980b9de632561ef24ee44ca9cab711b4040b402a40d243da01efcc0713e1759a51565cbc6e9e483526681308993e378b272e293c21b474c3f5a904b6c4dcd843c996730656e729553fd8384614ffc677f1b176e1194ccb82769e759e2be68e2ccbc693e8ecbac823bc490c0c29f7df4b54204f955b6384"
c3 = "32d71f5796d9fc3a42b1e1095470c007971ffd3ca3d6514a2cfe7eef5db21c78ff503cf1245ce82efe143c4ae04c86409c93c17da54bb360de6e4e49f54f11fe7691d03381745902bc6b3b0494115c7149c45e927ccd50723a05c9dcb873655c680028a3bf8bccb404f4d8774a2b4efd44bfac66091ed113229e29b5a076794f81641e6206e21cf0c30f1ae2863e2c84fbd88b37296498ab605ffec18e7ffabab69ad05849cac1590f01d01592c78ff952f59993a063dfebd0d4114de6ea523903b29ce2ea611c2a68c29b7e4bce218e142d319d805f06971ac7d0ad9cf2eefc101ac1d2c2c239e5a8d04278fd4947c295b31c86de48da9de00f4559f56c2b92"

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def part1(filename):
    with open(filename, 'r') as file:
        data = file.read()
    data = data.replace(":", "")
    data = data.replace(" ", "")
    data = data.replace("\n", "")
    data = int(data, 16)
    print(data)


part1("file.txt")

"""
n1 = 24024333509900754918918504952116864975126125908311896546098801562440649260224244924351392952815987412539261304682378039271110969398655318946507124857780930710329615794046877426969291480224417538230325888861393214705080648578689861908126043868642461236961583491866880865761079394964058246109597431684290825813193992881531532072488237528304547965063476937207772865729773049024783806601295872275143972309276670822440167716502616883175980070939465062525691685962307213337779283331387666346762424613174122880909563440958037380724965090866562638620374044216788329974541289723966093642151260357738139302203870759529650688347
n2 = 29377846774702184198925337039846334967067434261326607063416333980076595357031915025484834679220426609187984616215117407932712771976538758362547715478082335643088055664104356185793722117883931231652242368163396502413939236966011896776177199396691807851620973762062992157832889592077183593149922606298365414037520430986386012235916068875801683775560076008767425186985301012891027953700303954454130092092605240172817473022414968293315681008366672647768253951766061204233676947008306451713060755555936813725958452874358543368757030876828141145083895402174081124937468858034662998456480030621597201107597693670108691980707
n3 = 23577587684046707966380295377115733071785721606403699058865286187113812638568836764075088643042718056260174536775846420350859378445094951940589402178355491232723979774647149984763258617231669388345954709555720488933332112874271678178068927487155975168187380486613264602922858167887834496348069911573142748474376508949166038624594576799534861530225838503427247145953198245469410858990147401142758446420834461230834672254870222021724850602608691631284878054711676477214108874520310043640922085788981007002174689325948187082062194282509703310926773635381426433940450744848916759607238239748168232733532363556001560001517

#n = n1 * n2 * n3
#print(n)
n=16640665017929622533179174683031534337843384497899089226589437476849059428177208509306329246213268513188204424054921960005023035949752063238446509231342453217704479769283556303938588941540366255280116319386606670944747226989988753982299354312341134418143770933195857284434632028207870192560907075673672040710916506846530959285392732692569421884136867523646554153380864117446263667265626180649944526364942836876209347103308425764911201376215959473127277748812247509860661267843890940326161797507997271413301123197863281049561522314647257083486049985058131768656956465484298965411792309432489251124232019122019825798221282154457671579154700926043865090662100013138960244278293657688870521359195227298439532951233433246765196682973614081043139744435950910194776260141655991910662193916419063447795821127877508323118772726851464260309241948475359164300982155410511923133737588555615519763531026146986172577414018845557503867029865570304366617040913407354777993032038496037561765774871412340200544492123787703315115008439368751062329491998535178747879209883763662176512092403995461865994565186308625554712080593525919447176240152202867393841996351813509981164379506966740748864995780784282726220391116208377355602586503958254823277510239377460744641759484291769180478971139714911169322599352051400596680559673072882613718466785123117714920370433622952399267544282516655878264427403876711656031854407038663894514734011974005127730956326223950442006505652094087463918811639667074904590941067421238086078419379835698655043214898213760390412900868974338748820025170074969531039225341323618186693159048356000028758595647252885758341688555790718266096158220720364087287903998961672543177025589240052290356766632170628704734890300525335103288725588068346485877287869743495830276144779522524751723833111410400791413165941622276794349349408148915186059807515256093

m1 = gmpy2.f_div(n, n1)  # n / n1
m2 = gmpy2.f_div(n, n2)  #n/n2
m3 = gmpy2.f_div(n, n3) #n/n3

y1 = modinv(m1, n1)
y2 = modinv(m2, n2)
y3 = modinv(m3, n3)

print("yyy ")
print(y1)
print(y2)
print(y3)


x1 = mpz(c1) + mpz(m1) + mpz(y1)
#x2 = mpz.mul(c2, m2, y2)
#x3 = mpz.mul(c3, m3, y3)

#x = gmpy2.f_mod(x, n)

print("Le message est")
#print(x)

#print(x)


pc1 = int(c1, 16)
pc2 = int(c2, 16)
pc3 = int(c3, 16)

u1 = n2*n3
u2 = n1*n3
u3 = n1*n2

x = pc1*e1 + pc2*e2 + pc3*e3
print(x)
x = hex(x)
print(x)
s = x.replace("0x", "")
print(s)
#chaine = "b4a614cdad2daefc33244f931027f24ed62dac52a4635cd20c9156544d44d86093993192df2dd558315d10e7d85ee673a4094e4d7ab7e115cc477dc902232d3855fbdd58d81191572bd8db8d2fea142ce7d112c69db881ba0b50b5347959d8f8c70161e6d9ff0a482fdcf09df172215c299d5c36318e181e552c6daa8cf35b831a3a9e76e783cc1d4c32c9137106822dd89682027065233305d8ecfde2f95fe7b74a8807ffa53f82d8ed17f7db804a0e547d70e1e6ac5451c1da42145b174bbc59b10c622d50558d6ae41563cfca95c1efeb9c75930de8a7b4be8f424831aa79e7c6469486b3716b8c0278818fd9e7e10bf591fc90943a6436a0239714f6a76cea4dac0a61dae87fd98a596148d6cb67a41911344b913a03b4c9ffe6b7754f369c445768a16edb81355b9f24d8cc533217b17f2b4e71818e0abc58525b6484aba697b49f577984eb42086d96441ebcbf46635e562450ddf5417b16994c3e1a28b4cb55d2a31942a19ae24dcb515e9c5bf3e4872b513e99c1d442c395c5c8c15ada2d0b070017c875553090980b807a55a2bc4dd18dbd832c267b5cd2fcff63fb33b593448a9b5041522cdf0d17956f6286527c173ef7505593859de430993b6d27b804460fcec79e969a95626becdcdb70f2c385e87d4afa8cf7bd0020fa55701ac27383d6e1f263deb036f4e506e7772559f90b98105bae2651d5d60a58b64a3ef90f5582c09911e5fcafe1cbb2c0a6ceca6a94ea2d88d8195be6a57b2a774adcc1e0c56e1a17bbdfb2143b7e5e001d01c988731763a1532b238f4936afa786066ba5e28b79717e2292380f47c8840c20a2a44ae7ab7917ccdb1d36e972976696df19659f400c985ce15b3926f57c2a3a4526c90d050a26bed230d000852d4a295be4934106b19ce7b7e2951875ad38b740161a7f2b225975f4876aed4978ff8e44387b8bf6e71ac95feff49d003bcd735490a630d73a1d9f49013f24f6ab2080b1a09423dba0cc13d246156a078f8b3940acf6950cd612874b13520a7a482a5432f92753ae942cf32a7e2272135a079bc42b9d55df4b58a4fd7325d3a497ea"
#print(binascii.unhexlify(chaine))
"""