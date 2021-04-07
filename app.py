from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#Etusivu
@app.route("/")
def index():
    result = db.session.execute("SELECT COUNT(*) FROM Reseptit")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT R.id, R.nimi, SUM(A.hinta*O.maara), R.paivays FROM Reseptit R, Ohjeet O, Aineet A WHERE R.id=O.resepti_id AND O.aines_id=A.id GROUP BY R.id")
    recipes = result.fetchall()
    return render_template("index.html", count=count, recipes=recipes)

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
    nimi_ohje_paivays = db.session.execute("SELECT nimi, ohjeet, paivays FROM Reseptit WHERE id=:id", {"id":id}).fetchall()
    aines_hinta_maara = db.session.execute("SELECT A.nimi, A.hinta, O.maara FROM Aineet A, Ohjeet O WHERE O.resepti_id=:id AND A.id=O.aines_id", {"id":id}).fetchall()
    yhteishinta = db.session.execute("SELECT SUM(A.hinta*O.maara) FROM Aineet A, Ohjeet O WHERE O.resepti_id=:id AND A.id=O.aines_id", {"id":id}).fetchone()[0]
    return render_template("recipes.html", id=id, nimi_ohje_paivays=nimi_ohje_paivays, aines_hinta_maara=aines_hinta_maara, yhteishinta=yhteishinta)

@app.route("/deleterecipe/<int:id>")
def deleterecipe(id):
    db.session.execute("DELETE FROM Reseptit WHERE id=:id", {id:id})
    db.session.execute("DELETE FROM Ohjeet WHERE resepti_id=:id", {id:id})
    return redirect("/")

#Uusi resepti
@app.route("/uusi")
def uusi():
    result = db.session.execute("SELECT * FROM Aineet")
    ingred = result.fetchall()
    return render_template("new.html", ingred=ingred)


@app.route("/uusiresepti", methods=["POST"])
def send():
    nimi = request.form["nimi"]
    ohjeet = request.form["ohjeet"]
    sql1 = "INSERT INTO Reseptit (nimi, ohjeet) VALUES (:nimi, :ohjeet)"
    db.session.execute(sql1, {"nimi":nimi, "ohjeet":ohjeet})

    luku = db.session.execute("SELECT COUNT(*) FROM Aineet").fetchone()[0]
    sql2 = "INSERT INTO Ohjeet (resepti_id, aines_id, maara) VALUES (:resepti_id, :aines_id, :maara)"
    resepti_id = db.session.execute("SELECT id FROM Reseptit WHERE nimi=:nimi", {"nimi":nimi}).fetchone()[0]
    for i in range(1, luku):
        maara = int(request.form[f"maara{i}"])
        if maara >= 1:
            db.session.execute(sql2, {"resepti_id":resepti_id, "aines_id":i, "maara":maara})
    db.session.commit()
    return redirect("/")
