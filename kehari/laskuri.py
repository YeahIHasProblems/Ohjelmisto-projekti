import mysql.connector

#toivottavasti toimii
def laskuri():
    score = 1
    mult = 1
    xmult = 1
    sql = f"SELECT * FROM perks"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount >0 :
        for rivi in tulos:
            score += {rivi[0]}
            mult += {rivi[1]}
            xmult = xmult*{rivi[2]}
        tulos = score*mult*xmult
    return tulos


yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Tekn11kan1hmelaps1',
         autocommit=True
         )