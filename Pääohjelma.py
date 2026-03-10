import mysql.connector
import random

#muuttujia
lokaatio = ""
kierros = 0
tavoite = 0
kaupparoll = 0
kauppalist = []
kauppasecurity = 0
raha = 1000
perkvalinta = ""
perklist = []
palkka = 0
palkkastorage = 0
double = 0
roll = 0
common = ["Common1", "Common2", "Common3"]
rare = ["Rare1", "Rare2", "Rare3"]
epic = ["Epic1", "Epic2", "Epic3"]
supergamble = ["Jackpot1", "Jackpot2","Jackpot3"]

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='AdminST',
         autocommit=True
         )





def hae_satunnainen_lentokentta():
    sql = f"select airport.name as airport_name, country.name as country_name from airport join country on airport.iso_country = country.iso_country order by rand() limit 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if tulos:
        kentta = tulos[0]
    else:
        print("Lentokenttää ei löytynyt.")
    return kentta

def lokaatio_update(lokaatio):
    sql = f"UPDATE game SET location = (SELECT ident FROM airport WHERE name = '{lokaatio}') WHERE screen_name = 'Vesa' LIMIT 0;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
   
nimi = "Vesa"
def pelaajan_lokaatio(pelaaja):
    sql = f"SELECT name FROM airport, game where airport.ident = game.location and screen_name = '{pelaaja}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount >0 :
        for rivi in tulos:
            print(f"Uusi kohde on {rivi[0]}")
    return

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
        if kursori.rowcount >0 :
            for rivi in tulos:
                score += rivi[1]
                mult += rivi[2]
                xmult = xmult*rivi[3]
            tulos = score*mult*xmult
    return tulos


#valikko
def valikko():
    print(f"(1): Lennä toiseen paikkaan.\n(2): Avaa kauppa.\n(3): Osta perk\n(4): Lopeta peli.")
    print(f"Tavoite "+str(tavoite)+"/1000")
    valinta = input("Valitse numero (1)-(4)\n")
    return valinta

while True:
    valinta = valikko()
    if valinta == "1":
        lokaatio = hae_satunnainen_lentokentta()
        lokaatio_update(lokaatio)
        kierros += 1
        kauppasecurity = 0
        palkka = random.randint(5,2000)
        print("Tuleva palkka on "+ str(palkka))
        double = int(input("Paina 1 jos haluat tuplata. Paina 0 jos et halua tuplata: "))
        while double == 1:
            roll = random.randint(1,2)
            if roll == 1:
                palkka = (palkka * 2)
                print("Tuplaus onnistui, nykyinen palkka on "+ str(palkka))
            else:
                palkka = 0
                print("Tuplaus huti, hävisit kaiken")
                break
            double = int(input("Paina 1 jos haluat tuplata uudestaan tai paina 0 jos haluat jatkaa: "))
        raha += palkka
        print("Nykyinen rahatilanne: "+ str(raha))
        pelaajan_lokaatio(nimi)
        if len(perklist)> 0:
            tavoite += laskuri(perklist)
        if tavoite >= 1000:
            print("Voitit pelin")
            print(f"Sinulla kesti {str(kierros)} kierrosta!")
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
            perklist.append(kauppalist[perkvalinta-1])
            raha -= 1000
        else:
            print("Rahat ei riitä")
        print(f"Sinun perkit: {perklist}")
    elif valinta == "4":
        print("Lopetetaan ohjelma.")
        break
    else:
        print("Virhe")