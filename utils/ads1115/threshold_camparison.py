import numpy as np

def analyze_readings(off_readings, on_readings):
    off_mean = np.mean(off_readings)
    off_std = np.std(off_readings)
    on_mean = np.mean(on_readings)
    on_std = np.std(on_readings)
    
    print(f"Off Readings - Mean: {off_mean:.4f}, Std Dev: {off_std:.4f}")
    print(f"On Readings - Mean: {on_mean:.4f}, Std Dev: {on_std:.4f}")
    
    threshold = (off_mean + on_mean) / 2
    print(f"Suggested Threshold: {threshold:.4f}")
    
    return threshold

# Example usage
off_readings = [
    1.6491753288369395,
    1.6489253212073123,
    1.6488003173924985,
    1.6489253212073123,
    1.649050325022126,
    1.649050325022126,
    1.6489253212073123,
    1.6489253212073123,
    1.6489253212073123,
    1.6488003173924985,
    1.6491753288369395,
    1.649050325022126,
    1.6489253212073123,
    1.6493003326517535,
    1.6488003173924985,
    1.6489253212073123,
    1.6489253212073123,
    1.6488003173924985,
    1.6491753288369395,
    1.6489253212073123,
    1.649050325022126,
    1.6489253212073123,
    1.6488003173924985,
    1.649050325022126,
    1.6488003173924985,
    1.6486753135776848,
    1.6488003173924985,
    1.6489253212073123,
    1.6489253212073123,
    1.649050325022126,
    1.6486753135776848,
    1.6489253212073123,
    1.6488003173924985,
    1.6489253212073123,
    1.6491753288369395,
    1.6488003173924985,
    1.6488003173924985,
    1.649050325022126,
    1.6488003173924985,
    1.6489253212073123,
    1.6488003173924985,
    1.6489253212073123,
    1.6488003173924985,
    1.6488003173924985,
    1.6488003173924985,
    1.6489253212073123,
    1.649050325022126,
    1.6486753135776848,
    1.6488003173924985,
    1.649050325022126,
    1.6489253212073123,
    1.6489253212073123,
    1.649050325022126,
    1.649050325022126,
    1.649050325022126,
    1.6488003173924985,
    1.6488003173924985,
    1.649050325022126,
    1.6489253212073123,
    1.6488003173924985,
    1.6488003173924985,
    1.649050325022126,
    1.649050325022126,
    1.649050325022126,
    1.649050325022126,
    1.6486753135776848,
    1.6489253212073123,
    1.6489253212073123,
    1.6489253212073123,
    1.649050325022126,
    1.6486753135776848,
    1.6488003173924985,
    1.6489253212073123,
    1.6486753135776848,
    1.6489253212073123,
    1.6489253212073123,
    1.649050325022126,
    1.6488003173924985,
    1.649050325022126,
    1.6488003173924985,
    1.649050325022126,
    1.649050325022126,
    1.649050325022126,
    1.6489253212073123,
    1.6489253212073123,
    1.6491753288369395
]

on_readings = [
    1.7074271065401168,
    1.697426801355022,
    1.7043020111697744,
    1.6968017822809534,
    1.6940516983550522,
    1.6919266335032197,
    1.7000518814661092,
    1.7140523087252417,
    1.7163023773918882,
    1.7186774498733484,
    1.7241776177251504,
    1.7286777550584431,
    1.7313028351695303,
    1.7324278695028534,
    1.7333028962065493,
    1.7336779076509903,
    1.7305528122806482,
    1.7255526596881008,
    1.7233025910214546,
    1.707677114169744,
    1.7006769005401776,
    1.6773011871700187,
    1.6586756187627796,
    1.6420501113925596,
    1.635549913022248,
    1.6161743217261269,
    1.5950486770226142,
    1.5846733603930783,
    1.5741730399487288,
    1.5706729331339457,
    1.5697979064302499,
    1.5737980285042878,
    1.5837983336893826,
    1.5906735435041353,
    1.6089241004669332,
    1.6201744438001648,
    1.6429251380962555,
    1.6620507217627492,
    1.6834263740958892,
    1.702926969206824,
    1.7161773735770747,
    1.7234275948362683,
    1.7319278542435987,
    1.733427900021363,
    1.730677816095462,
    1.7213025299844356,
    1.7150523392437513,
    1.711177220984527,
    1.7026769615771966,
    1.6946767174291208,
    1.6825513473921934,
    1.6726760460219123,
    1.659800653096103,
    1.6573005767998292,
    1.6541754814294871,
    1.6448001953184606,
    1.6356749168370617,
    1.6329248329111608,
    1.6216744895779291,
    1.6019238868373669,
    1.5870484328745385,
    1.5776731467635121,
    1.5712979522080142,
    1.5702979216895046,
    1.5689228797265542,
    1.5719229712820828,
    1.5787981810968352,
    1.5936736350596639,
    1.5945486617633595,
    1.60067384868923,
    1.6241745658742028,
    1.6495503402813807,
    1.6738010803552354,
    1.6933016754661703,
    1.7059270607623525,
    1.7178024231696525,
    1.7248026367992186,
    1.7288027588732566,
    1.7319278542435987,
    1.7333028962065493,
    1.732677877132481,
    1.7309278237250891,
    1.7216775414288765,
    1.7135522934659873,
    1.7048020264290291,
    1.6918016296884062,
    1.6728010498367258,
    1.6591756340220343,
    1.6623007293923764,
    1.6574255806146427,
    1.658550614947966,
    1.6560505386516924,
    1.6434251533555102,
    1.6301747489852596,
    1.6181743827631458,
    1.6122992034669026,
    1.608174077578051,
    1.6044239631336406,
    1.6021738944669943,
    1.5975487533188881,
    1.5936736350596639,
    1.5914235663930174,
    1.5811732535782954,
    1.5762981048005615,
    1.5722979827265235,
    1.5700479140598773,
    1.5699229102450638,
    1.5779231543931396,
    1.5895485091708121,
    1.5989237952818385,
    1.6195494247260964,
    1.6287997070223093,
    1.632299813837092,
    1.6451752067629017,
    1.6511753898739585,
    1.662800744651631,
    1.6765511642811366,
    1.6959267555772577,
    1.6939266945402387,
    1.7089271523178808,
    1.7183024384289072,
    1.7281777397991884,
    1.7340529190954315,
    1.733427900021363,
    1.7288027588732566,
    1.7176774193548388,
    1.698926847132786,
    1.6824263435773796,
    1.671676015503403,
    1.6588006225775933,
    1.651800408948027,
    1.6475502792443617,
    1.6443001800592059,
    1.6295497299111912,
    1.624924588763085,
    1.6174243598742637,
    1.6060490127262186,
    1.6004238410596028,
    1.5944236579485458,
    1.5892985015411847,
    1.584423352763451,
    1.5764231086153753,
    1.5734230170598467,
    1.5732980132450332
]

threshold = analyze_readings(off_readings, on_readings)