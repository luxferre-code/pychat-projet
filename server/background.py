# Background file on Client

import sqlite3

database = 'db_server.db'

def id_in_db(idd: int) -> bool:
    """
    Fonction permettant de vérifier si un id est dans la base de donnée
    
    param:
    idd: integer
    
    Return type: boolean
    # Valentin Thuillier 
    """
    assert isinstance(idd, int), "L'id doit être un integer !"
    assert len(idd) == 10, "L'id spécifié n'est pas valide !"
    
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
    

def get_client(idd: int) -> tuple:
    """Récupère les informations du client ( nom et mail)
    Parameters:
        id : int
    # Juliann Lestrelin
    """
    
    assert type(idd) == int, "L'id est invalide"
    connexion = sqlite3.connect(database)
    cursor = connexion.cursor()
    cursor.execute("SELECT pseudo, mail FROM Clients WHERE id == ?", (idd,))
    c  = cursor.fetchone()
    connexion.commit()
    connexion.close()
    return c

def id_is_admin(idd: int) -> bool:
    """
    Fonction permettant de verifier si un id est un administrateur
    
    param:
    idd: integer
    
    Return type: boolean
    # Valentin Thuillier
    """
    #assert id_in_db(idd), "L'id spécifié n'existe pas !"
    try:
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute("SELECT count(id) FROM Admins WHERE id = ?", (str(idd), ))
        data = cursor.fetchone()
        if(data[0] == 1):
            connect.commit()
            connect.close()
            return True
        return False
    except:
        raise ConnectionError('Erreur survenu dans la recherche si l\'id est un administrateur')

def kick(idd: int) -> bool:
    """
    Fonction permettant de kick un utilisateur de PyChat grâce à son id
    
    param:
    idd: integer
    
    Return type: boolean
    # Valentin Thuillier
    """
    #assert id_in_db(idd), "L'id spécifié n'existe pas !"
    try:
        if(id_is_admin(idd)): return False
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        cursor.execute("DELETE FROM Clients WHERE id = ?", (idd, ))
        connect.commit()
        connect.close()
        return True
    except:
        return False