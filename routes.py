from app import app
import recipes
from flask import redirect, render_template, request
from db import db


#Etusivu
@app.route("/")
def index():
    count = recipes.reseptien_maara()
    tiedot = recipes.resepti_tiedot()
    return render_template("index.html", count=count, recipes=tiedot)

#Kirjautuminen
@app.route("/form", methods=["POST"])
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html",name=request.form["name"])

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
    for i in range(1, luku):
        maarat.append(int(request.form[f"maara{i}"]))
    recipes.lisaa_resepti(nimi, ohjeet, maarat)
    return redirect("/")