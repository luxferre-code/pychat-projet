# Background file on Clients

import sqlite3
from random import randint
import hashlib
import os
import sys
import pysftp
import pygame
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
    
def generate_send_file_name():
    temps = ''
    for _ in range(15):
        temps += chr(97 + randint(0, 26))
    return to_sha256(temps) + ".lxf"

def text_former(actual_text: str, event): # A refaire un peu :)
    if(event.type == pygame.KEYDOWN):
        if(event.key == 8): actual_text = actual_text[:-1]
        else: actual_text += chr(event.key)
    return actual_text

def get_reponse(name_file: str):
    with open('./receive/' + name_file, 'r', encoding='UTF-8') as file:
        rep = file.readline()
    if(rep == 'True'): final = True
    elif(rep == 'False'): final = False
    elif(rep == 'None'): final = None
    else: final = rep
    os.remove('./receive/' + name_file)
    return final

def send_file(file_name: str):
    user_client = ''
    password = ''
    ip = ''
    with pysftp.Connection(ip, username=user_client, password=password) as sftp:
        with sftp.cd('receive/'):
            sftp.put(file_name)
    return True

def read_config_file():
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
    if('config' in os.listdir()): os.remove('config')
    with open('config', 'a', encoding='UTF-8') as file:
        file.write(str(dico['auto_connect']) + '\n' + dico['username'] + '\n' + dico['password'])
    return True