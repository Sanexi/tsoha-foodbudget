CREATE TABLE Reseptit (id SERIAL PRIMARY KEY, nimi TEXT, ohjeet TEXT, paivays TIMESTAMPTZ DEFAULT Now());
INSERT INTO Reseptit (nimi, ohjeet) VALUES ('Makaronia ja jauhelihaa', 'Keitä makaronit, paista jauheliha ja sekoita.');
INSERT INTO Reseptit (nimi, ohjeet) VALUES ('Munakokkeli', 'Lisää munat ja kerma paistinpannulle ja sekoita, kunnes kiinteää');


CREATE TABLE Aineet (id SERIAL PRIMARY KEY, nimi TEXT, hinta DECIMAL);
INSERT INTO Aineet (nimi, hinta) VALUES ('Makaroni (400g)', 0.25);
INSERT INTO Aineet (nimi, hinta) VALUES ('Sika-nauta jauheliha (400g)', 2.25);
INSERT INTO Aineet (nimi, hinta) VALUES ('Kananmuna (1 kpl)', 0.14);
INSERT INTO Aineet (nimi, hinta) VALUES ('Ruokakerma (2 dl)', 0.40);

CREATE TABLE Ohjeet (id SERIAL PRIMARY KEY, resepti_id INTEGER, aines_id INTEGER, maara INTEGER);
INSERT INTO Ohjeet (resepti_id, aines_id, maara) VALUES (1, 1, 1);
INSERT INTO Ohjeet (resepti_id, aines_id, maara) VALUES (1, 2, 1);
INSERT INTO Ohjeet (resepti_id, aines_id, maara) VALUES (2, 3, 6);
INSERT INTO Ohjeet (resepti_id, aines_id, maara) VALUES (2, 4, 1);

CREATE TABLE Kayttajat (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'user');


