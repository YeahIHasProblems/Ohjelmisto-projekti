perklist = []
senzu = 3000
pate = 86
tolvanen = 67

slotcount = 3
def add_perk(newperk):
    if len(perklist) < slotcount:
        perklist.append(newperk)
    else:
        print("Perkkejä ei mahdu lisää!!")
    return perklist


print(perklist)