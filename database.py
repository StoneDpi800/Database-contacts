import sqlite3

def connecter():
    return sqlite3.connect("contacts.db")

def creer_table():
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            age INTEGER,
            adresse TEXT,
            code_postal TEXT,
            ville TEXT,
            photo BLOB
        )
    """)
    conn.commit()
    conn.close()


def ajouter(nom, prenom, age, adresse, code_postal, ville, photo=None):
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute(
        "INSERT INTO contacts (nom, prenom, age, adresse, code_postal, ville, photo) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nom, prenom, age, adresse, code_postal, ville, photo))
    conn.commit()
    conn.close()

def supprimer(id_nom):
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("DELETE FROM contacts WHERE id = ?", (id_nom,))
    conn.commit()
    conn.close()

def modifier(id, nom, prenom, age, adresse, code_postal, ville, photo=None):
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute(
        "UPDATE contacts SET nom=?, prenom=?, age=?, adresse=?, code_postal=?, ville=?, photo=? "
        "WHERE id=?",
        (nom, prenom, age, adresse, code_postal, ville, photo, id))
    conn.commit()
    conn.close()

def lire_contact(id_nom):
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM contacts WHERE id = ?", (id_nom,))
    resultat = curseur.fetchone()
    conn.close()
    return resultat

def lire_tous():
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM contacts")
    resultat = curseur.fetchall()
    conn.close()
    return resultat





def creer_table_historique():
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("""CREATE TABLE IF NOT EXISTS historique (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    action TEXT NOT NULL,
    nom TEXT NOT NULL)
                    """)
    conn.commit()
    conn.close()


def ajoute_historique(date, action, nom):
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("INSERT INTO historique (date, action, nom) VALUES (?, ?, ?)", (date, action, nom))
    conn.commit()
    conn.close()

def supprimer_historique(id):
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("DELETE FROM historique WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def supprimer_historique_all():
    conn = connecter()
    curseur = conn.cursor()

    curseur.execute("DELETE FROM historique")
    curseur.execute("DELETE FROM sqlite_sequence WHERE name = 'historique'")

    conn.commit()
    conn.close()

def lire_historique():
    conn = connecter()
    curseur = conn.cursor()
    curseur.execute("SELECT * FROM historique")
    resultat = curseur.fetchall()
    conn.close()
    return resultat



creer_table()
creer_table_historique()
print("Tables créées avec succès !")