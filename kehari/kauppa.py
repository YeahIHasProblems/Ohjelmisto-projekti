import random
common = ["Common1", "Common2", "Common3"]
rare = ["Rare1", "Rare2", "Rare3"]
epic = ["Epic1", "Epic2", "Epic3"]
supergamble = ["Jackpot1", "Jackpot2","Jackpot3"]
def kauppa():
    jackpot = random.randint(1,100)
    if jackpot > 0 and jackpot < 60:
        tuomio = (common[random.randint(0,random.randint(0,len(common)-1))])
    elif jackpot > 60 and jackpot < 85:
        tuomio = ((rare[random.randint(0,random.randint(0,len(rare)-1))]))
    elif jackpot > 85 and jackpot < 95:
        tuomio = ((epic[random.randint(0,random.randint(0,len(epic)-1))]))
    else:
        tuomio = ((supergamble[random.randint(0, random.randint(0, len(supergamble) - 1))]))
    return tuomio

print(kauppa())