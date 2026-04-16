import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)

def tallenna_peli():
    sql = """
        UPDATE game 
        SET money = %s, tavoite = %s, 
            location = (SELECT ident FROM airport WHERE name = %s LIMIT 1) 
        WHERE screen_name = %s
    """
    kursori = yhteys.cursor()
    kursori.execute(sql, (raha, tavoite, lokaatio, nimi))
    print(f"Peli tallennettu!")