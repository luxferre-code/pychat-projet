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

sftp_server = '89.86.152.239'
database = "db_server.db"

def make_client(pseudo: str, mail: str, pwd_no_crypted: str, send_file_name: str, author='0000000000') -> None: # a executé make_client(pseudo: str, password: str, mail: str)
    """
    Envoie de donnée de création du client au serveur
    Parameters:
        pseudo : str-> pseudo du client
        mail : str-> mail du client
        pwd_no_crypted : str-> mot de passe du client : pas en sha256
    Return:
        None
    # Juliann Lestrelin 22.02.2022
    """
    pwd_crypted = to_sha256(pwd_no_crypted)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + "\n" + author + "\nmake_client|" + pseudo + "/" + pwd_crypted + '/' + mail)

def get_client(idd: str):
    """Demande au serveur les informations sur l'utilisateur
    Parameters:
        id : string
    # Juliann Lestrelin 22.02.2022
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
    # Juliann Lestrelin 22.02.2022
    """
    return hashlib.sha256(bytes(pwd, 'utf-8')).hexdigest()

def good_login(username: str, password: str, send_file_name: str, author='0000000000') -> bool:
    """
    Fonction permettant de créer la requete pour vérifier les identifiants
    
    param:
    username: string (soit le pseudo ou bien le mail)
    password: string
    
    Return type: boolean
    # Valentin Thuillier 22.02.2022
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
    # Juliann Lestrelin 22.02.2022
    """
    # Créer un fichier avec comme ligne
    
    # nom_du_prochaine_fichier
    # author
    # commande|arg1/arg2/arg3/etc...

def get_id(username: str, password: str, send_file_name: str, author="0000000000") -> int:
    """
    Fonction qui permet de récuperer l'id d'un utilisateur grâce à son pseudo et son mot de passe
    
    param:
    username: string (soit le pseudo ou bien le mail)
    password: string
    
    Return type: int
    # Valentin Thuillier 22.02.2022
    """
    
    pwd_crypted = to_sha256(password)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + "\n" + author + "\nget_id|" + username + "/" + pwd_crypted)
        
def make_channel(name: str, send_file_name: str, password='', author='0000000000'):
    """
    Fonction permettant la création d'un salon

    param:
    name: String
    send_file_name: String
    password: String
    author: String

    Return type: None
    # Valentin Thuillier 11.03.2022
    """
    
    pwd_crypted = to_sha256(password)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + '\n' + author + '\nmake_channel|' + name + '/' + pwd_crypted)

def join_channel(id_channel: str, password: str, send_file_name: str, author='0000000000') -> None:
    """
    Fonction qui créer le fichier pour rejoindre un serveur
    param:
    id_channel: string
    password: string
    send_file_name: string
    author: string (author id)

    Return type: None
    # Valentin Thuillier 12/03/2022
    """
    pwd = to_sha256(password)

    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + '\n' + author + '\njoin_channel|' + id_channel + '/' + pwd + '/' + author)        

def modify_password(username: str, password: str, new_password: str, send_file_name: str, author='@Console') -> bool:
    """
    Fonction permettant la modification du mot de passe de son compte
    
    param:
    username: string
    password: string
    new_password: string
    
    Return type: bollean (True si effectuer, sinon False)
    # Valentin Thuillier 22.02.2022
    """
    assert isinstance(username, str), "Merci de rentrer comme identifiants un string !"
    assert isinstance(password, str), "Merci de rentrer comme mot de passe un string !"
    assert isinstance(new_password, str), "Merci de rentrer comme nouveau mot de passe un string !"
    
    pwd_crypted = to_sha256(new_password)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + "\n" + author + "\nmodify_password|" + username + "/" + pwd_crypted + "/" + new_password)

def name_channel(id_channel: str, send_file_name: str, author='0000000000'):
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + '\n' + author + '\nname_channel|' + id_channel)



def generate_send_file_name() -> str:
    """
    Cette fonction permet de generer le nom d'un fichier aléatoirement
    
    param:
    None
    
    Return type: string
    # Valentin Thuillier 26.02.2022
    """
    temps = ''
    for _ in range(15):
        temps += chr(97 + randint(0, 26))
    return to_sha256(temps) + ".lxf"

# def text_former(actual_text: str, event) -> str: # A refaire un peu :)
#     """
#     Fonction qui permet de capter les touches de clavier et de les mettre dans une chaine de caractere
#     
#     param:
#     actual_text: string
#     event: pygame.event
#     
#     Return type: string
#     # Valentin Thuillier
#     """
#     never_use = [1073741906, 1073741904, 1073741905, 1073741903, 127, 1073741901, 1073741902, 1073741899, 1073741898, 1073741897, 1073741896, 1073741895, 1073741894, 1073741893, 1073741892, 1073741891, 1073741890, 1073741889, 1073741888, 1073741887, 1073741886, 1073741885, 1073741884, 1073741883, 1073741882, 1073741881, 27, 178, 9, 1073742048, 1073742051, 1073742050, 32, 1073742048, 1073742054, 1073741925, 1073742052, 1073741907, 1073742049, 1073742053]
#     if(event.type == pygame.KEYDOWN):
#         if(event.key == pygame.K_PERIOD): actual_text += '.'
#         elif(event.key == pygame.K_AT): actual_text += '@'
#         elif(event.key == 8): actual_text = actual_text[:-1]
#         elif((event.key >= 97 and event.key <= 122) or (event.key >= 48 and event.key <= 57) and event.key not in never_use): actual_text += chr(event.key)
#         
#     return actual_text

def text_former(actual_text: str, event) -> str:
    """
    Fonction qui permet de capter les touches de clavier et de les mettre dans une chaine de caractere
    
    param:
    actual_text: string
    event: pygame.event
    
    Return type: string
    # Valentin Thuillier 27.02.2022
    """
    if(event.type == pygame.KEYDOWN):
        if(event.key == pygame.K_BACKSPACE): actual_text = actual_text[:-1]
        elif(event.key == pygame.K_HASH): actual_text += '#'
        elif(event.key == pygame.K_DOLLAR): actual_text += '$'
        elif(event.key == pygame.K_QUOTE): actual_text += '"'
        elif(event.key == pygame.K_LEFTPAREN): actual_text += '('
        elif(event.key == pygame.K_RIGHTPAREN): actual_text += ')'
        elif(event.key == pygame.K_ASTERISK or event.key == pygame.K_KP_MULTIPLY): actual_text += '*'
        elif(event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS): actual_text += '+'
        elif(event.key == pygame.K_COMMA): actual_text += ','
        elif(event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS): actual_text += '-'
        elif(event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE): actual_text += '/'
        elif(event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD): actual_text += '.'
        elif(event.key == pygame.K_AT): actual_text += '@'
        elif(event.key == pygame.K_EURO): actual_text += '€'
        elif(event.key == pygame.K_KP_ENTER or event.key == pygame.K_TAB): actual_text += '@'
        elif((event.key >= 97 and event.key <= 122) or (event.key >= 48 and event.key <= 57)): actual_text += chr(event.key)
        elif(event.key == pygame.K_SPACE): actual_text += ' '
        
    return actual_text

def get_reponse(name_file: str):
    """
    Fonction qui permet de lire le fichier renvoyer par le serveur
    
    param:
    name_file: string
    
    Return type: Any 
    # Valentin Thuillier 01.03.2022
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
    # Valentin Thuillier 01.03.2022
    """
    username = 'valjul'
    password = 'bp2022pjt'
    cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~', '.ssh', 'fake_known_hosts')))
    cnopts.hostkeys = None
    with pysftp.Connection(host=sftp_server, username=username, password=password, private_key=".ppk", cnopts=cnopts) as sftp:
        print('Envoie en cours...')
        sftp.put('./send/' + file_name, './server/receive/' + file_name)
        print('Envoyer')
    os.remove('./send/' + file_name)
    
def get_file(file_name: str) -> bool:
    """
    Fonction qui permet de récuperer un fichier sur le serveur
    param:
    file_name: str (.lxf in)
    
    Return type: boolean
    # Valentin Thuillier 01.03.2022
    """
    username = 'valjul'
    password = 'bp2022pjt'

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(host=sftp_server, username=username, password=password, private_key=".ppk", cnopts=cnopts) as sftp:
            sftp.get('./server/send/' + file_name,'./receive/' + file_name)
            sftp.remove('./server/send/' + file_name)
        return True
    except:
        return False


def read_config_file() -> dict:
    """
    Fonction permettant la lecture du fichier config et de renvoyer ces valeurs
    
    param:
    None
    
    Return type: dict
    # Valentin Thuillier 03.03.2022
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
    # Valentin Thuillier 03.03.2022
    """
    if('config' in os.listdir()): os.remove('config')
    with open('config', 'a', encoding='UTF-8') as file:
        file.write(str(dico['auto_connect']) + '\n' + dico['username'] + '\n' + dico['password'])
    return True

def remove_config_file():
    """
    Fonction permettant de supprimer le fichier de configuration
    
    param:
    None
    
    Return type: None
    # Valentin Thuillier 03.03.2022
    """
    if('config' in os.listdir()):
        os.remove('config')
        
def make_channel(name, send_file_name, password='', author='0000000000'):
    """
    Fonction permettant de créer le fichier à envoyer au serveur pour creer un channel
    
    param:
    name: String
    send_file_name: String
    password: String
    author: String
    
    Return type: None
    # Valentin Thuillier 08.03.2022
    """
    pwd_crypted = to_sha256(password)
    
    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + "\n" + author + "\nmake_channel|" + name + "/" + pwd_crypted)
    
def get_chat_channel(id_channel: str, send_file_name: str, author='0000000000'):
    """
    Fonction qui permet de lire les données récupére sur le channel
    # Valentin Thuillier 12.03.2022
    """
    with open('./send/' + send_file_name, 'a' ,encoding='UTF-8') as file:
        file.write(send_file_name + '\n' + author + '\nget_chat|' + id_channel)

def add_message(message: str, id_channel: str, send_file_name: str, author='0000000000'):
    """
    # Valentin Thuillier 12.03.2022
    """

    with open('./send/' + send_file_name, 'a', encoding='UTF-8') as file:
        file.write(send_file_name + '\n' + author + '\n' + 'add_message|' + id_channel + '/' + message)

def formater_chat_to_pg(file_name: str) -> list:
    """
    # Valentin Thuillier 13.03.2022
    """
    final = []
    temps = []
    t = ''
    
    with open('./receive/' + file_name, 'r', encoding='UTF-8') as file: temps = file.readlines()
    
    pygame.init()
    font = pygame.font.Font('./font/BlackWay.otf', 25)

    for elt in temps:
        final.append(font.render(elt[:-1], True, (255,255,255)))
    
    final.reverse()

    return final

get_chat_channel('5919121999', 'test.lxf')