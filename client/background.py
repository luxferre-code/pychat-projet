# Background file on Clients

import sqlite3
from random import randint
import hashlib

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

def get_client(idd: str):
    """Récupère les informations du client ( nom et mail)
    Parameters:
        id : string
    # Juliann Lestrelin
    """
    
    assert type(idd) == str, "L'id est invalide"
    connexion = sqlite3.connect(database)
    cursor = connexion.cursor()
    cursor.execute("SELECT pseudo, mail FROM Clients WHERE id = ?", (idd,))
    c  = cursor.fetchone()
    connexion.commit()
    connexion.close()
    return c
    

def to_sha256(pwd: str)->str:
    """Transformation du mot de passe en sha256 (sécurité)
    Parameter:
        pwd : str
    Return:
        str
    # Juliann Lestrelin
    """
    return hashlib.sha256(bytes(pwd, 'utf-8')).hexdigest()

def good_login(username: str, password: str) -> bool:
    """
    Fonction permettant de vérifier les identifiants de connexion
    
    param:
    username: string (soit le pseudo ou bien le mail)
    password: string
    
    Return type: boolean
    # Valentin Thuillier
    """
    assert isinstance(username, str), "Merci de rentrer comme identifiants un string !"
    assert isinstance(password, str), "Merci de rentrer comme mot de passe un string !"
    
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute('SELECT id FROM Clients WHERE pseudo = ? AND password = ?', (username, password))
    if(cursor.fetchone() != None): return True
    cursor.execute('SELECT id FROM Clients WHERE mail = ? AND password = ?', (username, password))
    if(cursor.fetchone() != None): return True
    return False

def change_name(idd: str,nwpsd: str):
    """Permet de changer le pseudo de l'utilisateur
    
    Parameters:
        idd : int -> id de l'utilisateur
        nwpsd : str -> nouveau pseudo de l'utilisateur
    # Juliann Lestrelin
    """
    
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("UPDATE Clients SET pseudo = ? WHERE id = ?", (nwpsd, idd))
    connect.commit()
    connect.close()

def get_id(username: str, password: str) -> int:
    """
    Fonction qui permet de récuperer l'id d'un utilisateur grâce à son pseudo / mail et son mot de passe
    
    param:
    username: string (soit le pseudo ou bien le mail)
    password: string
    
    Return type: int
    # Valentin Thuillier
    """
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    
    cursor.execute('SELECT id FROM Clients WHERE pseudo = ? AND password = ?', (username, password))
    if(cursor.fetchone != None):
        data = cursor.fetchone()[0]
        connect.commit()
        connect.close()
        return data
    cursor.execute('SELECT id FROM Clients WHERE pseudo = ? AND password = ?', (username, password))
    if(cursor.fetchone != None):
        data = cursor.fetchone()[0]
        connect.commit()
        connect.close()
        return data
    return None

def modify_password(username: str, password: str, new_password: str) -> bool:
    """
    Fonction permettant la modification du mot de passe de son compte
    
    param:
    username: string (soit le pseudo ou bien le mail)
    password: string
    new_password: string
    
    Return type: bollean (True si effectuer, sinon False)
    # Valentin Thuillier
    """
    assert isinstance(username, str), "Merci de rentrer comme identifiants un string !"
    assert isinstance(password, str), "Merci de rentrer comme mot de passe un string !"
    assert isinstance(new_password, str), "Merci de rentrer comme nouveau mot de passe un string !"
    
    if(good_login(username, password)):
        try:
            connect = sqlite3.connect(database)
            cursor = connect.cursor()
            cursor.execute('UPDATE Clients SET password = ? WHERE id = ?', (new_password ,get_id(username, password)))
            connect.commit()
            connect.close()
            return True
        except:
            return False
            print('Erreur sur la modification du mot de passe !')
    else:
        return False