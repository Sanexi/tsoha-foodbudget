from app import app
import recipes
import users
from flask import redirect, render_template, request, session
from db import db
from os import getenv


app.secret_key = getenv("SECRET_KEY")

#Etusivu
@app.route("/")
def index():
    count = recipes.reseptien_maara()
    tiedot = recipes.resepti_tiedot()
    return render_template("index.html", count=count, recipes=tiedot)

#Kirjautuminen
@app.route("/rekisterointi")
def rekisterointi():
    return render_template("rekisterointi.html")

@app.route("/lisaakayttaja", methods=["POST"])
def lisaakayttaja():
    username = request.form["username"]
    password = request.form["password"]
    users.uusi_kayttaja(username, password)
    session["username"] = username
    return redirect("/")

@app.route("/kirjautuminen", methods=["POST"])
def kirjautuminen():
    username = request.form["username"]
    password = request.form["password"]
    if users.vanha_kayttaja(username, password):
        session["username"] = username
    return redirect("/")

@app.route("/kirjaudu_ulos")
def kirjaudu_ulos():
    del session["username"]
    return redirect("/")


#Näytä reseptit
@app.route("/resepti/<int:id>")
def resepti(id):
    nimi_ohje_paivays = recipes.nimi_ohje_paivays(id)
    aines_hinta_maara = recipes.aines_hinta_maara(id)
    yhteishinta = recipes.yhteishinta(id)
    return render_template("recipes.html", id=id, nimi_ohje_paivays=nimi_ohje_paivays, aines_hinta_maara=aines_hinta_maara, yhteishinta=yhteishinta)

@app.route("/deleterecipe/<int:id>")
def deleterecipe(id):
    recipes.poista_resepti(id)
    return redirect("/")

#Uusi resepti
@app.route("/uusi")
def uusi():
    ingred = recipes.nayta_aineet()
    return render_template("new.html", ingred=ingred)


@app.route("/uusiresepti", methods=["POST"])
def send():
    nimi = request.form["nimi"]
    ohjeet = request.form["ohjeet"]
    maarat = []
    luku = recipes.aineiden_maara()
    for i in range(1, luku+1):
        maarat.append(int(request.form[f"maara{i}"]))
    recipes.lisaa_resepti(nimi, ohjeet, maarat)
    return redirect("/")