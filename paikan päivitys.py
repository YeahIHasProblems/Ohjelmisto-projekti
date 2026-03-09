import mysql.connector


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)

def paivita_uusi_sijainti(pelin_id):
    kursori = yhteys.cursor()

    sql_haku = "SELECT ident, name FROM airport ORDER BY RAND() LIMIT 1;"
    kursori.execute(sql_haku)
    uusi_lentokentta = kursori.fetchone()

    if uusi_lentokentta:
        uusi_ident = uusi_lentokentta['ident']
        uusi_nimi = uusi_lentokentta['name']


        sql_paivitys = "UPDATE game SET location = %s WHERE id = %s;"
        kursori.execute(sql_paivitys, (uusi_ident, pelin_id))

        print(f"Sijainti päivitetty!")
        print(f"Uusi lentokenttä: {uusi_nimi} ({uusi_ident})")
    else:
        print("Virhe: Lentokenttiä ei löytynyt.")


paivita_uusi_sijainti(1)