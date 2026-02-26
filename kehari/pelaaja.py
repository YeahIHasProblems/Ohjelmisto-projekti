import mysql.connector

nimi = "Vesa"
def pelaajan_lokaatio(pelaaja):
    sql = f"SELECT name FROM airport, game where airport.ident = game.location and screen_name = '{pelaaja}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount >0 :
        for rivi in tulos:
            print(f"{rivi[0]}")
    return

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Tekn11kan1hmelaps1',
         autocommit=True
         )

pelaajan_lokaatio(nimi)



