import mysql.connector
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='AdminST',
         autocommit=True
         )

käyttäjänimi = input("Mikä on nimesi: ")
def pelaaja(käyttäjänimi):
    sql = f"SELECT screen_name FROM game where screen_name = '{käyttäjänimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount >0 :
        for rivi in tulos:
            continue
    else:
        print("Anna oikea nimi")
    return
if pelaaja(käyttäjänimi) != "None":
    print(f"Tervetuloa pelaamaan {käyttäjänimi}")
