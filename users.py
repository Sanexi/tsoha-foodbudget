from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def uusi_kayttaja(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Kayttajat (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return vanha_kayttaja(username, password)

def vanha_kayttaja(username, password):
    sql = "SELECT password, username FROM Kayttajat WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = user[1]
            return True
        else:
            return False

def kayttajanimi():
    return session.get("username",0)

def kirjaudu_ulos():
    del session["username"]