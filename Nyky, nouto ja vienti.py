import mysql.connector

# 1. Create the connection first so the function can use it
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)

def hae_satunnainen_lentokentta():
    # Haetaan satunnainen lentokenttä
    sql = f"select airport.name as airport_name, country.name as country_name from airport join country on airport.iso_country = country.iso_country order by rand() limit 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


alkupiste = hae_satunnainen_lentokentta()
if alkupiste:
    print(f"Olet nyt täällä: {alkupiste[0]} ({alkupiste[1]})")

noutopiste = hae_satunnainen_lentokentta()
if noutopiste:
    print(f" Noutopaikka on: {noutopiste[0]} ({noutopiste[1]})")

maaranpaa = hae_satunnainen_lentokentta()
if maaranpaa:
    print(f"Viemiskohde on: {maaranpaa[0]} ({maaranpaa[1]}) ")

hae_satunnainen_lentokentta()