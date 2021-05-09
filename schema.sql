CREATE TABLE Reseptit (id SERIAL PRIMARY KEY, nimi TEXT UNIQUE, ohjeet TEXT, kayttaja TEXT, paivays TIMESTAMPTZ DEFAULT Now());

CREATE TABLE Aineet (id SERIAL PRIMARY KEY, nimi TEXT, hinta DECIMAL);

CREATE TABLE Ohjeet (id SERIAL PRIMARY KEY, resepti_id INTEGER references Reseptit(id), aines_id INTEGER references Aineet(id), maara INTEGER);

CREATE TABLE Kayttajat (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'user');


