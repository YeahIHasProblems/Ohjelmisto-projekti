import mysql.connector

def hae_satunnainen_lentokentta():
    sql = f"select airport.name as airport_name, country.name as country_name from airport join country on airport.iso_country = country.iso_country order by rand() limit 1;"
    print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[1]

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='AdminST',
    autocommit=True
)
haluttupaikka = hae_satunnainen_lentokentta()
print(haluttupaikka)
