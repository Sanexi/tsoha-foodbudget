from app import app
import recipes
import users
from flask import redirect, render_template, request, session, abort
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
        return render_template("error.html", message="Rekisteröinti ei onnistunut")

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

@app.route("/deleterecipe/<int:id>", methods=["POST"])
def deleterecipe(id):
    recipes.poista_resepti(id)
    return redirect("/")

#Uusi resepti
@app.route("/uusiresepti")
def uusi():
    ingred = recipes.nayta_aineet()
    return render_template("newrecipe.html", ingred=ingred)

@app.route("/lisaaresepti", methods=["POST"])
def lisaaresepti():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    nimi = request.form["nimi"]
    ohjeet = request.form["ohjeet"]

    if len(nimi) > 50:
        return render_template("error.html", message="Reseptin nimi on liian pitkä")
    if len(nimi) < 3:
        return render_template("error.html", message="Reseptin nimi on liian lyhyt")
    if len(ohjeet) > 1000:
        return render_template("error.html", message="Reseptin ohjeet ovat liian pitkät")

    maarat = {}
    ei_tyhjia = False
    luku = recipes.aineet_id()
    for i in luku:
        maarat[i] = int(request.form[f"maara{i}"])
        if maarat[i] > 0:
            ei_tyhjia = True

    if ei_tyhjia == False:
        return render_template("error.html", message="Reseptillä ei yhtään aineksia")

    kayttaja = session["username"]

    try:
        recipes.lisaa_resepti(nimi, ohjeet, maarat, kayttaja)
        return redirect("/")
    except:
        return render_template("error.html", message="Reseptin luonnissa virhe. Tarkista ettei reseptiä ole jo olemassa.") 

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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    nimimaara = request.form["nimimaara"]
    hinta = request.form["hinta"]

    if len(nimimaara) > 50:
        return render_template("error.html", message="Aineksen nimi on liian pitkä")
    if len(nimimaara) < 3:
        return render_template("error.html", message="Aineksen nimi on liian lyhyt. Muista ilmoittaa myös aineksen määrä")
    if "(" not in nimimaara or ")" not in nimimaara:
        return render_template("error.html", message="Anna aineksen määrä sulkeissa. Esim. jauheliha (400g)")
    if "€" in hinta or "," in hinta or " " in hinta or len(hinta) > 10 or "." not in hinta or len(hinta) < 2:
        return render_template("error.html", message="Hinta väärin. Anna hinta muodossa EUROT.SENTIT (Ei euromerkkiä). Esim. 2.50 tai 0.85")

    recipes.lisaa_aines(nimimaara, hinta)
    return redirect("/uusiresepti")