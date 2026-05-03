import mysql.connector
import random

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='AdminST',
    autocommit=True
)
common = ["Common1", "Common2", "Common3"]
rare = ["Rare1", "Rare2", "Rare3"]
epic = ["Epic1", "Epic2", "Epic3"]
supergamble = ["Jackpot1", "Jackpot2", "Jackpot3"]


def hae_satunnainen_lentokentta():
    sql = """SELECT airport.name FROM airport ORDER BY RAND() LIMIT 1;"""
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0] if tulos else "Tuntematon kenttä"


def lokaatio_update(lokaatio, pelaaja="Vesa"):
    sql = """UPDATE game SET location = (SELECT ident FROM airport WHERE name = %s) WHERE screen_name = %s;"""
    kursori = yhteys.cursor()
    kursori.execute(sql, (lokaatio, pelaaja))


def hae_pelaajan_lokaatio(pelaaja="Vesa"):
    sql = """SELECT airport.name FROM airport JOIN game ON airport.ident = game.location WHERE screen_name = %s;"""
    kursori = yhteys.cursor()
    kursori.execute(sql, (pelaaja,))
    tulos = kursori.fetchone()
    return tulos[0] if tulos else None


def kauppa_roll():
    jackpot = random.randint(1, 100)

    if jackpot < 60:
        return random.choice(common)
    elif jackpot < 85:
        return random.choice(rare)
    elif jackpot < 95:
        return random.choice(epic)
    else:
        return random.choice(supergamble)


def hae_perkin_tiedot(perk):
    sql = "SELECT * FROM perks WHERE name = %s"
    kursori = yhteys.cursor()
    kursori.execute(sql, (perk,))
    return kursori.fetchone()


def laskuri(perklist):
    score = 0
    mult = 0
    xmult = 1

    for perk in perklist:
        sql = "SELECT * FROM perks WHERE name = %s"
        kursori = yhteys.cursor()
        kursori.execute(sql, (perk,))
        tulos = kursori.fetchone()

        if tulos:
            score += tulos[1]
            mult += tulos[2]
            xmult *= tulos[3]

    return score * mult * xmult
