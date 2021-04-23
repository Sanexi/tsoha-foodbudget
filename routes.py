from app import app
import recipes
import users
from flask import redirect, render_template, request
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
    if users.uusi_kayttaja(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Rekisteröinti ei onnistunut. Käyttäjänimi saattaa olla valittu")

@app.route("/kirjautuminen", methods=["POST"])
def kirjautuminen():
    username = request.form["username"]
    password = request.form["password"]
    if users.vanha_kayttaja(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")

@app.route("/kirjaudu_ulos")
def kirjaudu_ulos():
    users.kirjaudu_ulos()
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
@app.route("/uusiresepti")
def uusi():
    ingred = recipes.nayta_aineet()
    return render_template("newrecipe.html", ingred=ingred)

#ONGELMA
@app.route("/lisaaresepti", methods=["POST"])
def lisaaresepti():
    nimi = request.form["nimi"]
    ohjeet = request.form["ohjeet"]
    maarat = {}
    luku = recipes.aineet_id()
    for i in luku:
        maarat[i] = int(request.form[f"maara{i}"])
    print(maarat)
    recipes.lisaa_resepti(nimi, ohjeet, maarat)
    return redirect("/")
#ONGELMA

@app.route("/deleteingred/<int:id>")
def deleteingred(id):
    recipes.poista_aines(id)
    return redirect("/uusiresepti")

#Uusi aines
@app.route("/uusiaines")
def uusiaines():
    ingred = recipes.nayta_aineet()
    return render_template("newingred.html", ingred=ingred)

@app.route("/lisaaaines", methods=["POST"])
def lisaaaines():
    nimimaara = request.form["nimimaara"]
    hinta = request.form["hinta"]
    recipes.lisaa_aines(nimimaara, hinta)
    return redirect("/uusiresepti")