import mysql.connector


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)


def hae_nykyinen_sijainti(pelaaja):
    kursori = yhteys.cursor()


    sql = f"SELECT airport.name, airport.ident  FROM airport, game WHERE airport.ident = game.location AND game.screen_name = '{pelaaja}' "

    kursori.execute(sql)
    tulos = kursori.fetchone()

    if tulos:
        nimi, koodi = tulos
        print(f"Pelaaja {pelaaja} on tällä hetkellä paikassa: {nimi} ({koodi})")
        return koodi
    else:
        print(f"Pelaajaa {pelaaja} ei löytynyt tai sijaintia ei ole asetettu.")
        return None




pelaajan_nimi = "Vesa"
nykyinen_koodi = hae_nykyinen_sijainti(pelaajan_nimi)