import mysql.connector
import random


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='lentopeli',
    user='elviira',
    password='tattu',
    autocommit=True,
    charset='utf8mb4',
    collation='utf8mb4_general_ci'
)


nimi = ""
lokaatio = ""
kierros = 0
tavoite = 0
raha = 1000
kauppasecurity = 0
kauppalist = []
perklist = []
kaupparoll = 0


common = ["common1", "common2", "common3"]
rare = ["rare1", "rare2", "rare3"]
epic = ["epic1", "epic2", "epic3"]
supergamble = ["jackpot1", "jackpot2", "jackpot3"]



def register():
    kayttaja = input("Anna uusi käyttäjänimi: ")
    salasana = input("Anna uusi salasana: ")
    try:
        kursori = yhteys.cursor()
        peli_id = random.randint(1, 100000)
        sql = "INSERT INTO game (id, screen_name, password, money, tavoite, location) VALUES (%s, %s, %s, 1000, 0, 'EFHK')"
        kursori.execute(sql, (peli_id, kayttaja, salasana))
        print(f"Käyttäjä {kayttaja} luotu ja peli alustettu!")
    except mysql.connector.Error:
        print("Virhe: Käyttäjänimi on jo varattu.")


def login():
    global nimi, raha, tavoite, lokaatio


    kursori = yhteys.cursor()
    kursori.execute("SELECT screen_name FROM game")
    kaikki_pelaajat = kursori.fetchall()

    print("\n--- REKISTERÖIDYT KÄYTTÄJÄT ---")
    if kaikki_pelaajat:
        for pelaaja in kaikki_pelaajat:
            print(f"- {pelaaja[0]}")
    else:
        print("(Ei vielä rekisteröityneitä käyttäjiä)")
    print("-------------------------------\n")


    kayttaja = input("Käyttäjänimi: ")
    salasana = input("Salasana: ")


    sql = "SELECT screen_name, money, tavoite, location FROM game WHERE screen_name = %s AND password = %s"
    kursori.execute(sql, (kayttaja, salasana))
    tulos = kursori.fetchone()

    if tulos:
        nimi, raha, tavoite, lokaatio = tulos
        print(f"Tervetuloa takaisin {nimi}!")
        return True
    else:
        print("Väärä nimi tai salasana.")
        return False


def tallenna_peli():
    sql = "UPDATE game SET money = %s, tavoite = %s, location = (SELECT ident FROM airport WHERE name = %s LIMIT 1) WHERE screen_name = %s"
    kursori = yhteys.cursor()
    kursori.execute(sql, (raha, tavoite, lokaatio, nimi))
    print(f"Peli tallennettu!")


def valikko():
    print(f"(1): Lennä toiseen paikkaan.\n(2): Avaa kauppa.\n(3): Osta perk\n(4): Lopeta peli.")
    print(f"Tavoite " + str(tavoite) + "/1000")
    valinta = input("Valitse numero (1)-(4)\n")
    return valinta


def hae_satunnainen_lentokentta():

    sql = "SELECT name FROM airport ORDER BY RAND() LIMIT 1"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if tulos:
        return tulos[0]


def lokaatio_update(uusi_kentta_nimi):
    sql = "UPDATE game SET location = (SELECT ident FROM airport WHERE name = %s LIMIT 1) WHERE screen_name = %s"
    kursori = yhteys.cursor()
    kursori.execute(sql, (uusi_kentta_nimi, nimi))
    yhteys.commit()


def pelaajan_lokaatio(pelaaja):
    sql = f"SELECT name FROM airport, game where airport.ident = game.location and screen_name = '{pelaaja}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        for rivi in tulos:
            print(f"Uusi kohde on {rivi[0]}")
    return


def kauppa():
    jackpot = random.randint(1, 100)
    if jackpot > 0 and jackpot < 60:
        tuomio = (common[random.randint(0, random.randint(0, len(common) - 1))])
    elif jackpot > 60 and jackpot < 85:
        tuomio = ((rare[random.randint(0, random.randint(0, len(rare) - 1))]))
    elif jackpot > 85 and jackpot < 95:
        tuomio = ((epic[random.randint(0, random.randint(0, len(epic) - 1))]))
    else:
        tuomio = ((supergamble[random.randint(0, random.randint(0, len(supergamble) - 1))]))
    return tuomio


def perktulostus(perk):
    sql = f"SELECT * FROM perks WHERE name='{perk}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        for rivi in tulos:
            print(
                f"-------------------------------------------\nNimi: {rivi[0]} Score: {rivi[1]} Mult: {rivi[2]} XMult: {rivi[3]}\n-------------------------------------------")
        return


def laskuri(perklist):
    score = 0
    mult = 0
    xmult = 1
    for i in perklist:
        sql = f"SELECT * FROM perks where name = '{i}'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if kursori.rowcount > 0:
            for rivi in tulos:
                score += rivi[1]
                mult += rivi[2]
                xmult = xmult * rivi[3]
            tulos = score * mult * xmult
    return tulos


# --- 3. PÄÄOHJELMA ---

if __name__ == "__main__":
    while True:
        print("\n1. Register \n2. Login \n3. Exit")
        choice = input("Valitse vaihtoehto: ")

        if choice == '1':
            register()
        elif choice == '2':
            if login():
                while True:
                    valinta = valikko()
                    if valinta == "1":
                        lokaatio = hae_satunnainen_lentokentta()
                        lokaatio_update(lokaatio)
                        kierros += 1
                        kauppasecurity = 0
                        palkka = random.randint(5, 2000)
                        print("Tuleva palkka on " + str(palkka))

                        double = int(input("Paina 1 jos haluat tuplata. Paina 0 jos et halua tuplata: "))
                        while double == 1:
                            roll = random.randint(1, 2)
                            if roll == 1:
                                palkka = (palkka * 2)
                                print("Tuplaus onnistui, nykyinen palkka on " + str(palkka))
                            else:
                                palkka = 0
                                print("Tuplaus huti, hävisit kaiken")
                                break
                            double = int(input("Paina 1 jos haluat tuplata uudestaan tai paina 0 jos haluat jatkaa: "))

                        raha += palkka
                        print("Nykyinen rahatilanne: " + str(raha))
                        pelaajan_lokaatio(nimi)

                        if len(perklist) > 0:
                            tavoite += laskuri(perklist)

                        if tavoite >= 1000:
                            print("Voitit pelin")
                            print(f"Sinulla kesti {str(kierros)} kierrosta!")
                            tallenna_peli()
                            break

                    elif valinta == "2" and kauppasecurity == 0:
                        kauppalist.clear()
                        while kaupparoll < 3:
                            kauppalist.append(kauppa())
                            perktulostus(kauppalist[-1])
                            kaupparoll += 1
                        kaupparoll = 0
                        kauppasecurity = 1

                    elif valinta == "3":
                        perkvalinta = int(input("Minkä vaihtoehdon haluaisit ostaa (1-3): "))
                        if raha >= 1000:
                            perklist.append(kauppalist[perkvalinta - 1])
                            raha -= 1000
                        else:
                            print("Rahat ei riitä")
                        print(f"Sinun perkit: {perklist}")

                    elif valinta == "4":
                        tallenna_peli()
                        print("Kirjauduttu ulos.")
                        break
        elif choice == '3':
            break