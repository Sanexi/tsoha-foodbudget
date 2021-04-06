

#Varmistus koodi

@app.route("/uusi/varmistus", methods=["POST"])
def uusi_varmistus():
    nimi = request.form["nimi"]
    ohjeet = request.form["ohjeet"]

    luku = db.session.execute("SELECT COUNT(*) FROM Aineet").fetchone()[0]
    ainekset = []
    for i in range(1, luku):
        maara = int(request.form[f"maara{i}"])
        if maara >= 1:
            aines_nimi = db.session.execute("SELECT nimi FROM Aineet WHERE id=:i", {"i":i}).fetchone()[0]
            aines_hinta =db.session.execute("SELECT hinta FROM Aineet WHERE id=:i", {"i":i}).fetchone()[0]
            aines_maara = (aines_nimi, aines_hinta, maara)
            ainekset.append(aines_maara)

    return render_template("new_confirm.html", nimi=nimi, ohjeet=ohjeet, ainekset=ainekset)