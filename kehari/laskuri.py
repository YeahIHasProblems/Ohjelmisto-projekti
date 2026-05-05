import mysql.connector
perklist = []
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Tekn11kan1hmelaps1',
         autocommit=True
         )
#toivottavasti toimii
def laskuri(perklist):
    score = 1
    mult = 1
    xmult = 1
    for i in perklist:
        sql = f"SELECT * FROM perks where name = '{perklist[i-1]}'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if kursori.rowcount >0 :
            for rivi in tulos:
                score += {rivi[1]}
                mult += {rivi[2]}
                xmult = xmult*{rivi[3]}
            tulos = score*mult*xmult
    return tulos

