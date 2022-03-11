# Background file on Server

import sqlite3
from datetime import datetime
import sys
from random import randint
import os

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
    cursor.execute('SELECT id FROM Clients WHERE id = ?', (idd, ))
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
    
def ban(idd: str, user="0000000000"):
    """ Banni l'utilisateur renseigné
    Parameters:
        idd : str -> id de l'utilisateur
    
    
    # Juliann Lestrelin
    """
    assert id_in_db(idd), "L'id renseigné n'existe pas"
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute("SELECT mail FROM Clients WHERE id = ?", (idd,))
    c = cursor.fetchone()
    cursor.execute("INSERT INTO Banni VALUES (?)", (c[0],))
    cursor.execute("DELETE FROM Clients WHERE id = ?", (idd,))
    server_logger("L'administrateur " + str(get_client(user)[0]) + " (" + idd + " ) vient de bannir " + c[0])
    connect.commit()
    connect.close()

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
        
# Création d'un client

def create_unique_id() -> str:
    """
    Fonction permettant de créer un id unique pour un utilisateur
    
    param:
    None
    
    Return type: string
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
    return str(temps)

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
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    idd = str(create_unique_id())
    cursor.execute('INSERT INTO Clients VALUES (?, ?, ?, ?)', (idd, pseudo, password, mail))
    server_logger("Un compte vient d'être créer ! " + pseudo + " (" + idd + ")")
    connect.commit()
    connect.close()
    return True

def get_id(username: str, password: str):
    """
    Fonction permettant de récupérer l'id d'un utilisateur grâce à son mail
    
    param:
    mail: str
    
    Return type: str
    # Valentin Thuillier
    """
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute('SELECT id FROM Clients WHERE pseudo = ? AND password = ?', (username, password))
    data = cursor.fetchone()
    connect.commit()
    connect.close()
    return data[0]

def good_login(username: str, password: str) -> bool:
    """
    Fonction permettant de vérifier si les informations données par l'utilisateur sont valides
    
    param:
    username: str
    password: str
    
    Return type: boolean
    # Valentin Thuillier
    """
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute('SELECt id FROM Clients WHERE pseudo = ? AND password = ?', (username, password))
    if(cursor.fetchone() != None): return True
    else: return False

    
def affiche_all_clients():
    """
    Fonction permettant l'affichage dans le shell de tous les clients mit sur le serveur
    
    param:
    None
    
    Return type: None
    # Valentin Thuillier
    """
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    cursor.execute('SELECT id, pseudo, mail, password FROM Clients')
    for elt in cursor.fetchall():
        print(elt)
        
def generate_id_channel():
    os.chdir('./channels/')
    final = ''
    for _ in range(10):
        final += str(randint(0, 9))
    if(final in os.listdir()): generate_id_channel
    else:
        os.chdir('../')
        return final
        
        
def make_channel(channel_name: str, password: str, author='0000000000') -> bool:
    """
    Fonction permetannt la création d'un salon dans le serveur

    param:
    channel_name: String
    password: String
    author: String (id owner)
    
    Return type: True if is good
    # Valentin Thuillier
    """
    try:
        id_channel = generate_id_channel()
        os.mkdir('./channels/ ' + id_channel)
        os.chdir('./channels/ ' + id_channel)
        
        with open('transmittion.lxf', 'a', encoding='UTF-8'):
            pass
        
        connect = sqlite3.connect('db_channel.db')
        cursor = connect.cursor()
        
        cursor.execute('CREATE TABLE Banni (id PRIMARY KEY NOT NULL)')
        cursor.execute('CREATE TABLE Member (id PRIMARY KEY NOT NULL)')
        
        connect.commit()
        
        cursor.execute('INSERT INTO Member VALUES (?)', (author, ))
        
        connect.commit()
        connect.close()
        
        os.chdir('../..')
        
        connect = sqlite3.connect(database)
        cursor = connect.cursor()
        
        cursor.execute('INSERT INTO Channels VALUES(?, ?, ?, ?)', (id_channel, channel_name, password, author))
        
        connect.commit()
        connect.close()
        return True
    except:
        return False

def get_transmittion_channel(id_channel: str):
    os.chdir('./channels')
    if(id_channel not in os.listdir()):
        os.chdir('..')
        return False
    os.chdir('./channels/' + id_channel)
    with open('transmittion.txt', 'r', encoding='UTF-8') as file:
        all_file = file.readlines()
    return all_file

print(get_transmittion_channel('7283282626'))