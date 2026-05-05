import mysql.connector



yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)




def tallenna_peli(nimi, raha, tavoite, lokaatio_nimi):
    sql = """UPDATE game SET money = %s, tavoite = %s, location = (SELECT ident FROM airport WHERE name = %s LIMIT 1) WHERE screen_name = %s"""
    kursori = yhteys.cursor()
    kursori.execute(sql, (raha, tavoite, lokaatio_nimi, nimi))


def tallenna():
    if "pelaaja" in session:
        tallenna_peli(
            session["pelaaja"],
            session["raha"],
            session["tavoite"],
            session["lokaatio"]
        )
        return jsonify({"success": True, "message": "Peli tallennettu tietokantaan!"})
    return jsonify({"success": False, "message": "Ei kirjautunutta käyttäjää."})