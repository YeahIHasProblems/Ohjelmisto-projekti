from flask import Flask, render_template, redirect, url_for, session, request
import random
from pelinlogiikka import hae_satunnainen_lentokentta, kauppa_roll, laskuri, common, rare, epic, supergamble, pullcard, \
    deckreset, maakoodi

app = Flask(__name__)
app.secret_key = "taavoiollamikavaa"


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
    session.setdefault("kierros", 0)
    session.setdefault("tavoite", 0)
    session.setdefault("raha", 1000)
    session.setdefault("perklist", [])
    session.setdefault("kauppalist", [])
    session.setdefault("kauppasecurity", 0)
    session.setdefault("palkka", 0)
    session.setdefault("double_active", False)
    session.setdefault("lokaatio", "")
    session.setdefault("blackjackplayer", 0)
    session.setdefault("blackjackdealer", 0)
    session.setdefault("lippu", "")


@app.route("/")
def index():
    init_game()
    return render_template("index.html")


@app.route("/lento", methods=["GET", "POST"])
def lento():
    init_game()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "start":
            session["lokaatio"] = hae_satunnainen_lentokentta()
            session["palkka"] = random.randint(5, 2000)
            session["double_active"] = True
            session["double_message"] = ""
            session["kierros"] += 1
            session["kauppalist"] = []
            session["kauppasecurity"] = 0
            session["lippu"] = lippugenerator()
            return redirect(url_for("lento"))

        if action == "double":
            roll = random.randint(1, 2)
            if roll == 1:
                session["palkka"] *= 2
                session["double_message"] = "Tuplaus onnistui!"
            else:
                session["palkka"] = 0
                session["double_message"] = "Tuplaus epäonnistui!"
                session["double_active"] = False
            return redirect(url_for("lento"))

        if action == "stop_double":
            session["raha"] += session["palkka"]

            if session["perklist"]:
                session["tavoite"] += laskuri(session["perklist"])

            if session["tavoite"] >= 1000:
                return redirect(url_for("voitto"))

            session["double_active"] = False
            session["double_message"] = ""
            session["lokaatio"] = ""
            session["palkka"] = 0

            return redirect(url_for("lento"))

    return render_template("lento.html")


@app.route("/kauppa")
def kauppa_sivu():
    init_game()
    if session["kauppasecurity"] == 0:
        session["kauppalist"] = [kauppa_roll() for _ in range(3)]
        session["kauppasecurity"] = 1
    return render_template(
        "kauppa.html",
        common=common,
        rare=rare,
        epic=epic,
        supergamble=supergamble
    )


@app.route("/osta_perk", methods=["POST"])
def osta_perk():
    init_game()
    index = int(request.form.get("index"))
    perk_nimi = session["kauppalist"][index]
    if perk_nimi in common:
        hinta = 300
    elif perk_nimi in rare:
        hinta = 800
    elif perk_nimi in epic:
        hinta = 1500
    else:
        hinta = 3000
    if session["raha"] >= hinta:
        session["perklist"].append(perk_nimi)
        session["raha"] -= hinta

    return redirect(url_for("kauppa_sivu"))


@app.route("/voitto")
def voitto():
    kierrokset = session.get("kierros", 0)

    reset_game()

    return render_template("voitto.html", kierrokset=kierrokset)


deck = []


@app.route("/blackjack", methods=["GET", "POST"])
def blackjack():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "hit" and session["blackjackplayer"] < 22:
            session["blackjackplayer"] += pullcard()
            if session["blackjackdealer"] <= 16:
                session["blackjackdealer"] += pullcard()
            if session["blackjackdealer"] > 21 and session["blackjackplayer"] < 21:
                session["raha"] += 100
                blackjackreset()
            if session["blackjackdealer"] < 21 and session["blackjackplayer"] > 21:
                session["raha"] -= 100
                blackjackreset()
            if session["blackjackdealer"] > 21 and session["blackjackplayer"] > 21:
                blackjackreset()

        if action == "stay":
            if session["blackjackdealer"] > session["blackjackplayer"]:
                session["raha"] -= 100
                blackjackreset()
            if session["blackjackdealer"] < session["blackjackplayer"]:
                session["raha"] += 100
                blackjackreset()
            else:
                blackjackreset()
    return render_template("blackjack.html")


def blackjackreset():
    deck.append(deckreset)
    session["blackjackdealer"] = 0
    session["blackjackplayer"] = 0


def lippugenerator():
    lokaatio = session["lokaatio"]

    if isinstance(lokaatio, dict):
        koodi = maakoodi(lokaatio["name"])
    else:
        koodi = maakoodi(lokaatio)

    lippu = f"https://flagsapi.com/{koodi}/flat/64.png"
    return lippu


if __name__ == "__main__":
    import random

    app.run(debug=True, port=5000)