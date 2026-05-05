import random
import re
deck = ["D2","D3","D4","D5","D6","D7","D8","D9","D10","D10","D10","D11",
        "H2","H3","H4","H5","H6","H7","H8","H9","H10","H10","H10","H11",
        "C2","C3","C4","C5","C6","C7","C8","C9","C10","C10","C10","C11",
        "S2","S3","S4","S5","S6","S7","S8","S9","S10","S10","S10","S11"
        ]


def pullcard():
    draw = random.randint(0,(len(deck)-1))
    card = deck[draw]
    country = re.findall("\\w", card)[0]
    value = re.findall("\\d+", card)[0]
    deck.remove(deck[draw])
    return value




