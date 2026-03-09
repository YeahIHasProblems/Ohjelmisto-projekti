def remove_perk(perk):
    if perk in perklist:
        perklist.remove(perk)
    else:
        print("Perkkiä ei löydy listasta")
