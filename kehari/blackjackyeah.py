import random
import re
deck = ["2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AD",
        "2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","AH",
        "2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AC",
        "2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AS"
        ]
#value = re.findall("\\d+", card)[0]

def pullcard():
    draw = random.randint(0,(len(deck)-1))
    card = deck[draw]
    deck.remove(deck[draw])
    return card

def cardvalue(card):
    value = 0
    if any(char.isdigit() for char in card) == True:
        value = int(re.findall("\\d+", card)[0])
    elif card.find("A") != -1:
        value = 11
    else:
        value = 10
    return value

korttitunnus = pullcard()
kortti = f"https://deckofcardsapi.com/static/img/{korttitunnus}.png"
print(kortti)