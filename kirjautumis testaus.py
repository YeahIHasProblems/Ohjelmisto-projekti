def main():
    options = {'1':register, '2':login, '3': exit}
    while True:
        print ("\n1.Register \n2.Login\n3.Exit")
        choice=input("valitse vaihtoehto: ")
        action = options.get(choice)
        if action:
           tulos = action()

           if choice == '2' and tulos  is True:
               peli_kaynnissa = True
               while peli_kaynnissa == True:
                   valinta = valikko()
                   if valinta == '4':
                        print("Poistutaan pelistä...")
                        peli_kaynnissa = False
                    elif valinta == '1':
                        print("Lennetään...")
                    elif valinta == '2':
                        print("mene kauppaan...")
                    elif valinta == '3':
                        print("osta perk...")
        else:
            print("ei ole vaihtoehto")

if __name__ == "__main__":
    main()
