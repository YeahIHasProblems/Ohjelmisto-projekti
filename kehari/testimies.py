import mysql.connector

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
    sql = f"UPDATE game SET location = (SELECT ident FROM airport WHERE name = '{lokaatio}') WHERE screen_name = 'Vesa';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return


yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Tekn11kan1hmelaps1',
         autocommit=True
         )

testi = str(hae_satunnainen_lentokentta())
lokaatio_update(testi)