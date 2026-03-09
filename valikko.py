def valikko():
    print(f"(1): Lennä toiseen paikkaan.\n(2): Avaa kauppa.\n(3): Lopeta peli.")
    print(f"Tavoite 1000/1000")
    valinta = input("Valitse numero (1)-(3)\n")
    return valinta

while True:
    valinta = valikko()

    if valinta == "1":
        print("Lennetään toiseen paikkaan.")
        break
    elif valinta == "2":
        print("Avataan kauppa.")
        break
    elif valinta == "3":
        print("Lopetetaan ohjelma.")
        break
