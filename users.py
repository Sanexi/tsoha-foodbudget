from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def uusi_kayttaja(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO Kayttajat (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()

def vanha_kayttaja(username, password):
    sql = "SELECT password FROM Kayttajat WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            return True
        else:
            return False