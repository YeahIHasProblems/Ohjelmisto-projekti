from flask import Flask, render_template, request
app = Flask(__name__)

import mysql.connector
import random


#muuttujat
lokaatio = ""
kierros = 0
tavoite = 0
kaupparoll = 0
kauppalist = []
kauppasecurity = 0
raha = 1000
perkvalinta = ""
perklist = []
palkka = 0
palkkastorage = 0
double = 0
roll = 0
common = ["Common1", "Common2", "Common3"]
rare = ["Rare1", "Rare2", "Rare3"]
epic = ["Epic1", "Epic2", "Epic3"]
supergamble = ["Jackpot1", "Jackpot2","Jackpot3"]

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Tekn11kan1hmelaps1',
         autocommit=True
         )



#Nää app.route kohdat laittaa näkyviin noi halutut html sivut
@app.route('/')
@app.route('/userinterface.html')
def main():
    return render_template('userinterface.html')

@app.route('/page2.html')
def page2():
    return render_template('page2.html')

@app.route('/page3.html')
def page3():
    return render_template('page3.html')

#hakee satunnaisen lentokentän
def hae_satunnainen_lentokentta():
    sql = f"select airport.name as airport_name, country.name as country_name from airport join country on airport.iso_country = country.iso_country order by rand() limit 1;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if tulos:
        kentta = tulos[0]
    else:
        print("Lentokenttää ei löytynyt.")
    return kentta



app.run(use_reloader=True, host='127.0.0.1', port=3000)