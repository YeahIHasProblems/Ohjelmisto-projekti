import mysql.connector
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='AdminST',
         autocommit=True
         )
perklist = ["jackpot1","jackpot1","common3"]

def laskuri(perklist):
    score = 0
    mult = 0
    xmult = 1
    for i in perklist:
        sql = f"SELECT * FROM perks where name = '{i}'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if kursori.rowcount >0 :
            for rivi in tulos:
                score += rivi[1]
                mult += rivi[2]
                xmult = xmult*rivi[3]
            tulos = score*mult*xmult
    return tulos
print(laskuri(perklist))