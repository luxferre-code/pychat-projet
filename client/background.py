# Background file on Clients

import sqlite3
from random import randint

database = "db_server.db"

# Création d'un client

def create_unique_id() -> int:
    """
    Fonction permettant de créer un id unique pour un utilisateur
    
    param:
    None
    
    Return type: integer
    # Valentin Thuillier
    """
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    while True:
        temps = str(randint(0, 9))
        for _ in range(9):
            temps += str(randint(0, 9))
        cursor.execute('SELECT count(id) FROM Clients WHERE id = ?', (temps, ))
        data = cursor.fetchone()[0]
        if(data == 0): break
    return int(temps)

def make_client(pseudo: str, password: str, mail: str) -> bool:
    """
    Fonction permettant la création d'un utilisateur sur la base de donnée serveur
    
    param:
    pseudo: string (3 <= taille <= 12)
    password: string (crypté en sha256)
    mail: string
    
    Return type: boolean (True si réussit, False si pas réussi)
    # Valentin Thuillier
    """
    assert isinstance(pseudo, str) and len(pseudo) >= 3 and len(pseudo) <= 12, "Impossible de créer un compte client avec un pseudo ne respectant pas les régles !"
    assert isinstance(password, str), "Merci d'entrer un mot de passe crypté en sha256 !"
    assert isinstance(mail, str) and "@" in mail, "Merci d'entrer un mail valide !"
    
    try:
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Clients VALUES (?, ?, ?, ?)', (create_unique_id(), pseudo, password, mail))
        connect.commit()
        connect.close()
        return True
    except:
        return False

#Récupération info client

def get_client(idd: int):
    """Récupère les informations du client ( nom et mail)
    Parameters:
        id : int
    # Juliann Lestrelin
    """
    
    assert type(idd) == int, "L'id est invalide"
    connexion = sqlite3.connect(database)
    cursor = connexion.cursor()
    cursor.execute("SELECT name, mail FROM Clients WHERE id == ?", (idd,))
    
    return cursor.fechone()[0]
