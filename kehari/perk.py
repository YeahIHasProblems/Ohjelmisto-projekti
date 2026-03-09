import mysql.connector

#toivottavasti toimii
def perk(nimi):
    sql = f"SELECT * FROM perks WHERE name='{nimi}'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount >0 :
        for rivi in tulos:
            print(f"{rivi[0]}")
            print(f"{rivi[1]}")
            print(f"{rivi[2]}")
            print(f"{rivi[3]}")
    return


yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Tekn11kan1hmelaps1',
         autocommit=True
         )