import random
start = random.randrange(2)
print(start)
davidson= ["davidson",90,30,20]
harley = ["harley",100,25,25]

while(harley[1] > 0 and davidson[1] > 0):
    if(start == 0):
        #print(harley#[0], "atacou")
        dano = harley[2] - davidson[3]
        vida = harley[1] - dano
        print(vida)
        harley.remove(harley[1])
        harley.insert(1,vida)
    else:
        #print(davison[0], "atacou")
        dano = harley[2] - davidson[3]
        vida = harley[1] - dano
        print(vida)
        davidson.remove(davidson[1])
        davidson.insert(1,vida)
else:
    if(davidson[1] > 0):
        print(davidson[0], "ganhou")
    else:        
       print(harley[0], "ganhou")