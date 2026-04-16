import mysql.connector


def hae_satunnainen_lentokentta():
    # Valitaan satunnainen lentokenttä
    sql = "SELECT name FROM airport ORDER BY RAND() LIMIT 1"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if tulos:
        return tulos[0]


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)

hae_satunnainen_lentokentta()