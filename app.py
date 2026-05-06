from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from pelinlogiikka import (
    hae_satunnainen_lentokentta, kauppa_roll, laskuri,
    common, rare, epic, supergamble,
    pullcard, deckreset, maakoodi, cardvalue,
    tarkista_kirjautuminen, tallenna_peli, rekisteroi
)
import random

app = Flask(__name__)
app.secret_key = "taavoiollamikavaa"


# --- ALUSTUKSET ---
def reset_game():
    session["kierros"] = 0
    session["tavoite"] = 0
    session["raha"] = 1000
    session["perklist"] = []
    session["kauppalist"] = []
    session["kauppasecurity"] = 0
    session["palkka"] = 0
    session["double_active"] = False
    session["double_message"] = ""
    session["lokaatio"] = ""
    session["blackjackplayer"] = 0
    session["blackjackdealer"] = 0
    session["lippu"] = ""

def init_game():
    """Alustaa istunnon muuttujat, jos niitä ei ole jo asetettu (esim. kirjautumisen yhteydessä)."""
    defaults = {
        "kierros": 0,
        "tavoite": 0,
        "raha": 1000,
        "perklist": [],
        "kauppalist": [],
        "kauppasecurity": 0,
        "palkka": 0,
        "double_active": False,
        "lokaatio": "",
        "blackjackplayer": 0,
        "blackjackdealer": 0,
        "lippu": "",
        "playercard": "",
        "dealercard": ""
    }
    for key, val in defaults.items():
        session.setdefault(key, val)


def blackjackreset():
    """Nollaa blackjack-kädet ja pakan."""
    session["blackjackdealer"] = 0
    session["blackjackplayer"] = 0
    session["playercard"] = ""
    session["dealercard"] = ""
    deckreset()


# --- REITIT ---

@app.route("/")
def login_sivu():
    """Ohjaa suoraan peliin jos session on jo auki."""
    if "pelaaja" in session:
        return redirect(url_for("index"))
    return render_template("LOGINsivu.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    tulos = tarkista_kirjautuminen(username, password)

    if tulos:
        session["pelaaja"] = tulos[0]
        session["raha"] = tulos[1]
        session["tavoite"] = tulos[2]
        session["lokaatio"] = tulos[3]

        init_game()  # Alustetaan loput muuttujat (kierrokset, perkit jne.)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Väärä nimi tai salasana."})


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Täytä kaikki kentät."})


    onnistui = rekisteroi(username, password)

    if onnistui:
        return jsonify({"success": True, "message": "Käyttäjä luotu!"})
    else:
        return jsonify({"success": False, "message": "Käyttäjänimi on jo varattu."})

@app.route("/tallenna", methods=["POST"])
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


@app.route("/index")
def index():
    if "pelaaja" not in session: return redirect(url_for("login_sivu"))
    init_game()
    return render_template("index.html")


@app.route("/lento", methods=["GET", "POST"])
def lento():
    if "pelaaja" not in session: return redirect(url_for("login_sivu"))
    init_game()

    if request.method == "POST":
        action = request.form.get("action")
        if action == "start":
            session["lokaatio"] = hae_satunnainen_lentokentta()
            session["palkka"] = random.randint(5, 2000)
            session["double_active"] = True
            session["kierros"] += 1
            session["kauppasecurity"] = 0
            koodi = maakoodi(session["lokaatio"])
            session["lippu"] = f"https://flagsapi.com/{koodi}/flat/64.png"

        elif action == "double":
            if random.randint(1, 2) == 1:
                session["palkka"] *= 2
            else:
                session["palkka"] = 0
                session["double_active"] = False

        elif action == "stop_double":
            session["raha"] += session["palkka"]
            session["tavoite"] += laskuri(session["perklist"])
            if session["tavoite"] >= 1000: return redirect(url_for("voitto"))
            session["double_active"] = False
            session["palkka"] = 0

    return render_template("lento.html")


@app.route("/kauppa")
def kauppa_sivu():
    if "pelaaja" not in session: return redirect(url_for("login_sivu"))
    init_game()
    if session.get("kauppasecurity") == 0:
        session["kauppalist"] = [kauppa_roll() for _ in range(3)]
        session["kauppasecurity"] = 1
    return render_template("kauppa.html", common=common, rare=rare, epic=epic, supergamble=supergamble)


@app.route("/osta_perk", methods=["POST"])
def osta_perk():
    idx = request.form.get("index")
    if idx is not None:
        perk = session["kauppalist"][int(idx)]
        hinta = 300 if perk in common else 800 if perk in rare else 1500 if perk in epic else 3000
        if session["raha"] >= hinta:
            session["perklist"].append(perk)
            session["raha"] -= hinta
    return redirect(url_for("kauppa_sivu"))


@app.route("/blackjack", methods=["GET", "POST"])
def blackjack():
    if "pelaaja" not in session: return redirect(url_for("login_sivu"))
    init_game()

    if request.method == "POST":
        action = request.form.get("action")
        if action == "hit" and session["blackjackplayer"] < 22:
            p_card = pullcard()
            session["playercard"] = f"https://deckofcardsapi.com/static/img/{p_card}.png"
            session["blackjackplayer"] += cardvalue(p_card)

            if session["blackjackdealer"] <= 16:
                d_card = pullcard()
                session["blackjackdealer"] += cardvalue(d_card)
                session["dealercard"] = f"https://deckofcardsapi.com/static/img/{d_card}.png"


            if session["blackjackplayer"] > 21 or session["blackjackdealer"] > 21:
                if session["blackjackplayer"] <= 21:
                    session["raha"] += 100
                else:
                    session["raha"] -= 100
                blackjackreset()

        elif action == "stay":

            if session["blackjackplayer"] > session["blackjackdealer"]:
                session["raha"] += 100
            else:
                session["raha"] -= 100
            blackjackreset()

    return render_template("blackjack.html")


@app.route("/perkit")
def perkit():
    if "pelaaja" not in session: return redirect(url_for("login_sivu"))
    init_game()
    return render_template("perkit.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_sivu"))

@app.route("/voitto")
def voitto():
    kierrokset = session.get("kierros", 0)

    reset_game()

    return render_template("voitto.html", kierrokset=kierrokset)

if __name__ == "__main__":
    app.run(debug=True)