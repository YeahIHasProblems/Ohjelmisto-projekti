import mysql.connector


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)

def paivita_lokaatio(pelaaja, uusi_ident):

    kursori = yhteys.cursor()

    sql = "UPDATE game SET location = %s WHERE screen_name = %s"
    kursori.execute(sql, (uusi_ident, pelaaja))
    kursori.close()

def pelaajan_lokaatio(pelaaja):

    sql = f"SELECT name FROM airport, game WHERE airport.ident = game.location AND screen_name = '{pelaaja}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount > 0:
        for rivi in tulos:
            print(f"Pelaaja {pelaaja} on nyt paikassa: {rivi[0]}")
    kursori.close()

# --- Testaus ---
nimi = "Vesa"
uusi_kentta = "EFHK" # Esimerkki: Helsinki-Vantaa

# 1. Päivitetään paikka
paivita_lokaatio(nimi, uusi_kentta)

# 2. Tarkistetaan uusi nimi tulostamalla se
pelaajan_lokaatio(nimi)