from flask import Flask, render_template, redirect, url_for, session, request
from pelinlogiikka import hae_satunnainen_lentokentta, kauppa_roll, laskuri

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
    return render_template("kauppa.html")

@app.route("/osta_perk", methods=["POST"])
def osta_perk():
    init_game()
    index = int(request.form.get("index"))
    hinta = 1000

    if session["raha"] >= hinta:
        try:
            perk_nimi = session["kauppalist"][index]
            session["perklist"].append(perk_nimi)
            session["raha"] -= hinta
        except IndexError:
            pass
    return redirect(url_for("perkit"))

@app.route("/perkit")
def perkit():
    init_game()
    return render_template("perkit.html")

@app.route("/voitto")
def voitto():
    kierrokset = session.get("kierros", 0)

    reset_game()

    return render_template("voitto.html", kierrokset=kierrokset)


if __name__ == "__main__":
    import random
    app.run(debug=True)

