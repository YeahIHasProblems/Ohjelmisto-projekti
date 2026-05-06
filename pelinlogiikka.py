import mysql.connector
import random
import re

# Tietokantayhteys
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='AdminST',
    autocommit=True
)

# --- KONFIGURAATIO ---
common = ["Common1", "Common2", "Common3"]
rare = ["Rare1", "Rare2", "Rare3"]
epic = ["Epic1", "Epic2", "Epic3"]
supergamble = ["Jackpot1", "Jackpot2", "Jackpot3"]

# Blackjack-pakka (Standardimuoto deckofcardsapi:lle)
initial_deck = [
    "2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AD",
    "2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","AH",
    "2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AC",
    "2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AS"
]
deck = initial_deck.copy()

# --- TIETOKANTAFUNKTIOT ---

def rekisteroi(kayttaja, salasana):
    try:
        kursori = yhteys.cursor()
        peli_id = random.randint(1, 100000)
        sql = "INSERT INTO game (id, screen_name, password, money, tavoite, location) VALUES (%s, %s, %s, 1000, 0, 'EFHK')"
        kursori.execute(sql, (peli_id, kayttaja, salasana))
        return True
    except mysql.connector.Error:
        return False

def tarkista_kirjautuminen(kayttaja, salasana):
    sql = "SELECT screen_name, money, tavoite, location FROM game WHERE screen_name = %s AND password = %s"
    kursori = yhteys.cursor()
    kursori.execute(sql, (kayttaja, salasana))
    return kursori.fetchone()

def tallenna_peli(nimi, raha, tavoite, lokaatio_nimi):
    sql = """UPDATE game SET money = %s, tavoite = %s, location = (SELECT ident FROM airport WHERE name = %s LIMIT 1) WHERE screen_name = %s"""
    kursori = yhteys.cursor()
    kursori.execute(sql, (raha, tavoite, lokaatio_nimi, nimi))




def hae_satunnainen_lentokentta():
    sql = "SELECT name FROM airport ORDER BY RAND() LIMIT 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0] if tulos else "Helsinki-Vantaa Airport"

def lokaatio_update(lokaatio_nimi, pelaaja):
    sql = "UPDATE game SET location = (SELECT ident FROM airport WHERE name = %s) WHERE screen_name = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (lokaatio_nimi, pelaaja))

def hae_pelaajan_lokaatio(pelaaja):
    sql = "SELECT airport.name FROM airport JOIN game ON airport.ident = game.location WHERE screen_name = %s;"
    kursori = yhteys.cursor()
    kursori.execute(sql, (pelaaja,))
    tulos = kursori.fetchone()
    return tulos[0] if tulos else None

def maakoodi(lentokentta_nimi):
    sql = "SELECT iso_country FROM airport WHERE name = %s"
    kursori = yhteys.cursor()
    kursori.execute(sql, (lentokentta_nimi,))
    tulos = kursori.fetchone()
    return tulos[0] if tulos else "FI"

# --- KAUPPA JA PERKIT ---

def kauppa_roll():
    jackpot = random.randint(1, 100)
    if jackpot < 60: return random.choice(common)
    elif jackpot < 85: return random.choice(rare)
    elif jackpot < 95: return random.choice(epic)
    else: return random.choice(supergamble)

def laskuri(perklist):
    score, mult, xmult = 0, 0, 1
    kursori = yhteys.cursor()
    for perk in perklist:
        sql = "SELECT score, mult, xmult FROM perks WHERE name = %s"
        kursori.execute(sql, (perk,))
        tulos = kursori.fetchone()
        if tulos:
            score += tulos[0]
            mult += tulos[1]
            xmult *= tulos[2]
    return score * (mult if mult > 0 else 1) * xmult

# --- BLACKJACK LOGIIKKA ---

def pullcard():
    global deck
    if not deck: deckreset()
    draw_idx = random.randint(0, len(deck) - 1)
    return deck.pop(draw_idx)

def cardvalue(card):
    digit_match = re.search(r"\d+", card)
    if digit_match: return int(digit_match.group())
    if "A" in card: return 11
    return 10

def deckreset():
    global deck
    deck = initial_deck.copy()
    return deck