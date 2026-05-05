
import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Tekn11kan1hmelaps1',
         autocommit=True
         )

def hae_satunnainen_lentokentta():
    sql = """SELECT airport.name FROM airport ORDER BY RAND() LIMIT 1;"""
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0] if tulos else "Tuntematon kenttä"

kenttä = hae_satunnainen_lentokentta()
print(kenttä)

koodi = "BE"
lippu = f"https://flagsapi.com/{koodi}/flat/64.png"

def maakoodi(nimi):
    sql = f"SELECT iso_country FROM airport WHERE name='{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount >0 :
        for rivi in tulos:
            pass
    return rivi[0]


koodi = maakoodi(kenttä)
print(koodi)





