from db import db

#ETUSIVULLE
#Reseptien määrä:
def reseptien_maara():
    result = db.session.execute("SELECT COUNT(*) FROM Reseptit")
    count = result.fetchone()[0]
    return count
#Reseptien tiedot
def resepti_tiedot():
    result = db.session.execute("SELECT R.id, R.nimi, SUM(A.hinta*O.maara), R.paivays, R.kayttaja FROM Reseptit R, Ohjeet O, Aineet A WHERE R.id=O.resepti_id AND O.aines_id=A.id GROUP BY R.id")
    recipes = result.fetchall()
    return recipes


#NÄYTÄ RESEPTIT
def nimi_ohje_paivays(id):
    palautus = db.session.execute("SELECT nimi, ohjeet, paivays, kayttaja FROM Reseptit WHERE id=:id", {"id":id}).fetchall()
    return palautus

def aines_hinta_maara(id):
    palautus = db.session.execute("SELECT A.nimi, A.hinta, O.maara FROM Aineet A, Ohjeet O WHERE O.resepti_id=:id AND A.id=O.aines_id", {"id":id}).fetchall()
    return palautus

def yhteishinta(id):
    palautus = db.session.execute("SELECT SUM(A.hinta*O.maara) FROM Aineet A, Ohjeet O WHERE O.resepti_id=:id AND A.id=O.aines_id", {"id":id}).fetchone()[0]
    return palautus
#Poista resepti:
def poista_resepti(id):
    db.session.execute("DELETE FROM Reseptit WHERE id=:id", {"id":id})
    db.session.execute("DELETE FROM Ohjeet WHERE resepti_id=:id", {"id":id})
    db.session.commit()


#UUSI RESEPTI
def nayta_aineet():
    result = db.session.execute("SELECT * FROM Aineet")
    ingred = result.fetchall()
    return ingred

def poista_aines(id):
    db.session.execute("DELETE FROM Aineet WHERE id=:id", {"id":id})
    db.session.execute("DELETE FROM Ohjeet WHERE aines_id=:id", {"id":id})
    db.session.commit()

def aineiden_maara():
    aineet = db.session.execute("SELECT COUNT(*) FROM Aineet").fetchone()[0]
    return aineet

def aineet_id():
    tulos = db.session.execute("SELECT id FROM Aineet").fetchall()
    palautus = []
    for i in tulos:
        palautus.append(i[0])
    return palautus

def lisaa_resepti(nimi, ohjeet, maarat, kayttaja):
    sql1 = "INSERT INTO Reseptit (nimi, ohjeet, kayttaja) VALUES (:nimi, :ohjeet, :kayttaja)"
    db.session.execute(sql1, {"nimi":nimi, "ohjeet":ohjeet, "kayttaja":kayttaja})
    luku = aineet_id()
    sql2 = "INSERT INTO Ohjeet (resepti_id, aines_id, maara) VALUES (:resepti_id, :aines_id, :maara)"
    resepti_id = db.session.execute("SELECT id FROM Reseptit WHERE nimi=:nimi", {"nimi":nimi}).fetchone()[0]
    for i in luku:
        maara = maarat[i]
        if maara >= 1:
            db.session.execute(sql2, {"resepti_id":resepti_id, "aines_id":i, "maara":maara})
    db.session.commit()


#UUSI AINES
def lisaa_aines(nimimaara, hinta):
    sql1 = "INSERT INTO Aineet (nimi, hinta) VALUES (:nimimaara, :hinta)"
    db.session.execute(sql1, {"nimimaara":nimimaara, "hinta":hinta})
    db.session.commit()
