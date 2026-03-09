
def add_perk(newperk):
    if len(perklist) < slotcount:
        perklist.append(newperk)
    else:
        print("Perkkejä ei mahdu lisää!!")
    return perklist

