# Background file on Clients

import sqlite3
from random import randint
import hashlib
import os
import sys
import pysftp
import pygame
from PIL import Image
# https://www.tutorialspoint.com/python_network_programming/python_sftp.htm

database = "db_server.db"

def make_client(pseudo: str, mail: str, pwd_no_crypted: str, send_file_name: str, author='@Console') -> None: # a executé make_client(pseudo: str, password: str, mail: str)
    """
    Envoie de donnée de création du client au serveur
    Parameters:
        pseudo : str-> pseudo du client
        mail : str-> mail du client
        pwd_no_crypted : str-> mot de passe du client : pas en sha256
    Return:
        None
    # Juliann Lestrelin
    """
    # Créer un fichier avec comme ligne
    
    # nom_du_prochaine_fichier
    # author
    # commande|arg1/arg2/arg3/etc...


#Récupération info client

def get_client(idd: str):
    """Demande au serveur les informations sur l'utilisateur
    Parameters:
        id : string
    # Juliann Lestrelin
    """
    # Créer un fichier avec comme ligne
    
    # nom_du_prochaine_fichier
    # author
    # commande|arg1/arg2/arg3/etc...
    

def to_sha256(pwd: str)->str:
    """Transformation du mot de passe en sha256 (sécurité)
    Parameter:
        pwd : str
    Return:
        str
    # Juliann Lestrelin
    """
    return hashlib.sha256(bytes(pwd, 'utf-8')).hexdigest()

def good_login(username: str, password: str, send_file_name: str, author='@Console') -> bool:
    """
    Fonction permettant de créer la requete pour vérifier les identifiants
    
    param:
    username: string (soit le pseudo ou bien le mail)
    password: string
    
    Return type: boolean
    # Valentin Thuillier
    """
    assert isinstance(username, str), "Merci de rentrer comme identifiants un string !"
    assert isinstance(password, str), "Merci de rentrer comme mot de passe un string !"
    
    pwd_crypted = to_sha256(password)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + "\n" + author + "\ngood_login|" + username + "/" + pwd_crypted)

def change_name(idd: str,nwpsd: str):
    """Permet de changer le pseudo d'un joueur
    
    Parameters:
        idd : int -> id de l'utilisateur
        nwpsd : str -> nouveau pseudo de l'utilisateur
    # Juliann Lestrelin
    """
    # Créer un fichier avec comme ligne
    
    # nom_du_prochaine_fichier
    # author
    # commande|arg1/arg2/arg3/etc...

def get_id(username: str, password: str, send_file_name: str, author="@Console") -> int:
    """
    Fonction qui permet de récuperer l'id d'un utilisateur grâce à son pseudo et son mot de passe
    
    param:
    username: string (soit le pseudo ou bien le mail)
    password: string
    
    Return type: int
    # Valentin Thuillier
    """
    
    pwd_crypted = to_sha256(password)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + "\n" + author + "\nget_id|" + username + "/" + pwd_crypted)
        

def modify_password(username: str, password: str, new_password: str, send_file_name: str, author='@Console') -> bool:
    """
    Fonction permettant la modification du mot de passe de son compte
    
    param:
    username: string
    password: string
    new_password: string
    
    Return type: bollean (True si effectuer, sinon False)
    # Valentin Thuillier
    """
    assert isinstance(username, str), "Merci de rentrer comme identifiants un string !"
    assert isinstance(password, str), "Merci de rentrer comme mot de passe un string !"
    assert isinstance(new_password, str), "Merci de rentrer comme nouveau mot de passe un string !"
    
    pwd_crypted = to_sha256(new_password)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + "\n" + author + "\nmodify_password|" + username + "/" + pwd_crypted + "/" + new_password)
    
def generate_send_file_name() -> str:
    """
    Cette fonction permet de generer le nom d'un fichier aléatoirement
    
    param:
    None
    
    Return type: string
    # Valentin Thuillier
    """
    temps = ''
    for _ in range(15):
        temps += chr(97 + randint(0, 26))
    return to_sha256(temps) + ".lxf"

def text_former(actual_text: str, event) -> str: # A refaire un peu :)
    """
    Fonction qui permet de capter les touches de clavier et de les mettre dans une chaine de caractere
    
    param:
    actual_text: string
    event: pygame.event
    
    Return type: string
    # Valentin Thuillier
    """
    never_use = [1073741906, 1073741904, 1073741905, 1073741903, 127, 1073741901, 1073741902, 1073741899, 1073741898, 1073741897, 1073741896, 1073741895, 1073741894, 1073741893, 1073741892, 1073741891, 1073741890, 1073741889, 1073741888, 1073741887, 1073741886, 1073741885, 1073741884, 1073741883, 1073741882, 1073741881, 27, 178, 9, 1073742048, 1073742051, 1073742050, 32, 1073742048, 1073742054, 1073741925, 1073742052, 1073741907, 1073742049, 1073742053]
    if(event.type == pygame.KEYDOWN):
        if(event.key == 8): actual_text = actual_text[:-1]
        elif((event.key >= 97 and event.key <= 122) or (event.key >= 48 and event.key <= 57) and event.key not in never_use): actual_text += chr(event.key)
    return actual_text

def get_reponse(name_file: str):
    """
    Fonction qui permet de lire le fichier renvoyer par le serveur
    
    param:
    name_file: string
    
    Return type: Any
    """
    with open('./receive/' + name_file, 'r', encoding='UTF-8') as file:
        rep = file.readline()
    if(rep == 'True'): final = True
    elif(rep == 'False'): final = False
    elif(rep == 'None'): final = None
    else: final = rep
    os.remove('./receive/' + name_file)
    return final

def send_file(file_name: str) -> bool:
    """
    Fonction permettant l'envoyer d'un fichier sur le serveur
    
    param:
    file_name: string
    
    Return type: bool
    """
    user_client = ''
    password = ''
    ip = ''
    try:
        with pysftp.Connection(ip, username=user_client, password=password) as sftp:
            with sftp.cd('receive/'):
                sftp.put(file_name)
        return True
    except:
        return False

def read_config_file() -> dict:
    """
    Fonction permettant la lecture du fichier config et de renvoyer ces valeurs
    
    param:
    None
    
    Return type: dict
    # Valentin Thuillier
    """
    dico = {'auto_connect': False,
            'username': '',
            'password': ''}
    
    if('config' not in os.listdir()): return dico
    
    with open('config', 'r', encoding='UTF-8') as file:
        temps = file.readline()
        if(temps[:-1] == 'True'): dico['auto_connect'] = True
        else: dico['auto_connect'] = False
        
        dico['username'] = file.readline()[:-1]
        dico['password'] = file.readline()
        
    return dico

def config_file(dico: dict):
    """
    Fonction qui permet de créer le fichier *config* qui contient des informations de connexion
    
    param:
    dico: dict avec comme clé
        *auto_connect*: bool
        *username*: string
        *password*: string
        
    Return type: True si la fonction a fonctionner
    # Valentin Thuillier
    """
    if('config' in os.listdir()): os.remove('config')
    with open('config', 'a', encoding='UTF-8') as file:
        file.write(str(dico['auto_connect']) + '\n' + dico['username'] + '\n' + dico['password'])
    return True