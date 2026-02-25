import mysql.connector




def hae_satunnainen_lentokentta():
    sql = f"select airport.name as airport_name, country.name as country_name from airport join country on airport.iso_country = country.iso_country order by rand() limit 1;"
    print(sql)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()

    if tulos:
        print(f"Noutopaikka löydetty!")
        print(f"Lentokenttä: {tulos[0]}")
        print(f"Maa: {tulos[1]}")
    else:
        print("Lentokenttää ei löytynyt.")


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)

hae_satunnainen_lentokentta()