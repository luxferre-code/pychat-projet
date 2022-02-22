# Background file on Client

import sqlite3
from datetime import datetime

database = 'db_server.db'

def id_in_db(idd: str) -> bool:
    """
    Fonction permettant de vérifier si un id est dans la base de donnée
    
    param:
    idd: string
    
    Return type: boolean
    # Valentin Thuillier 
    """
    assert isinstance(idd, str), "L'id doit être un string !"
    
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute('SELECT count(id) FROM Clients WHERE id = ?', (idd, ))
    if(cursor.fetchone() == None):
        connect.commit()
        connect.close()
        return False
    connect.commit()
    connect.close()
    return True
    

def get_client(idd: str) -> tuple:
    """Récupère les informations du client ( nom et mail)
    Parameters:
        id : str
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

def id_is_admin(idd: str) -> bool:
    """
    Fonction permettant de verifier si un id est un administrateur
    
    param:
    idd: string
    
    Return type: boolean
    # Valentin Thuillier
    """
    assert id_in_db(idd), "L'id spécifié n'existe pas !"
    try:
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute("SELECT count(id) FROM Admins WHERE id = ?", (idd, ))
        data = cursor.fetchone()
        if(data[0] == 1):
            connect.commit()
            connect.close()
            return True
        return False
    except:
        raise ConnectionError('Erreur survenu dans la recherche si l\'id est un administrateur')

def kick(idd: str, user="0000000000") -> bool:
    """
    Fonction permettant de kick un utilisateur de PyChat grâce à son id
    
    param:
    idd: string
    
    Return type: boolean
    # Valentin Thuillier
    """
    assert id_in_db(idd), "L'id spécifié n'existe pas !"
    try:
        if(id_is_admin(get_client(idd)[1])): return False
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        pseudo = get_client(idd)[0]
        cursor.execute("DELETE FROM Clients WHERE id = ?", (idd, ))
        connect.commit()
        connect.close()
        server_logger("L'administrateur " + str(get_client(user)[0]) + " (" + str(user) + ") vient de kick l'utilisateur " + pseudo + " (" + str(idd) + ")")
        return True
    except:
        return False

def add_admin(idd: str) -> bool:
    """
    Fonction permettant de mettre un utilisateur avec l'id spécifié en tant qu'administrateur PyChat

    param:
    idd: string

    Return type: boolean
    # Valentin Thuillier
    """
    if(not id_is_admin(get_client(idd)[1])):
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO Admins VALUES (?)", (get_client(idd)[1], ))
        connect.commit()
        connect.close()
        server_logger("Ajout de l'utilisateur " + str(get_client(idd)[0]) + " (" + str(idd) + ") en tant qu'administrateur PyChat")
        return True
    else:
        return False

def remove_admin(idd: str) -> bool:
    """
    Fonction permettant d'enlever les permissions administrateur à un utilisateur

    param:
    idd: string

    Return type: boolean
    # Valentin Thuillier
    """
    if(id_is_admin(get_client(idd)[1])):
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute("DELETE FROM Admins WHERE id = ?", (get_client(idd)[1], ))
        connect.commit()
        connect.close()
        server_logger("Suppresion de l'utilisateur " + str(get_client(idd)[0]) + " (" + str(idd) + ") en tant qu'administrateur PyChat")
        return True
    else:
        return False

def server_logger(string: str) -> None:
    """
    Fonction permettant d'enregistrer dans le fichier *logs.txt* des informations avec un heurodateur

    param:
    string: string

    Return type: None
    # Valentin Thuillier
    """
    assert isinstance(string, str), "Merci de spécifier un string !"
    with open('logs.txt', 'a', encoding='UTF-8') as file:
        file.write("[" + str(datetime.now()) + "] " + string + "\n")
