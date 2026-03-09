import mysql.connector
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='AdminST',
         autocommit=True
         )

def perktulostus():
        sql = f"SELECT * FROM perks WHERE name='jackpot1'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if kursori.rowcount >0 :
            for rivi in tulos:
                print(f"-------------------------------------------\nNimi: {rivi[0]} Score: {rivi[1]} Mult: {rivi[2]} XMult: {rivi[3]}\n-------------------------------------------")
        return
perktulostus()