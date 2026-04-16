import mysql.connector
import random


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)


nimi = ""
lokaatio = ""



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
    # ----------------------------------------------

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
