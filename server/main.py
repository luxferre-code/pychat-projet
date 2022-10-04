# Main file on Server
import background as bg
import os
import sys
from datetime import datetime
from time import time

"""
Error code:
    15: Trop de channels à nous
    4: Pseudo deja pris
    3: Mot de passe incorrect
    6: Mail incorrect
    1: Identifiant incorrect
    0: Caractere ou mot interdit
    9: Non propriétaire
    -1: Salon n'existe plus
"""

class Server:
    def __init__(self, database: str, logs: bool):
        self.__database = database
        self.__logs = logs
        self.__owner_account = ['0000000000']
        self.clear_folder('./receive/')
        self.clear_folder('./send/')
        self.__kids_securite = True
        
    def clear_folder(self, folder: str):
        for elt in os.listdir(folder):
            os.remove(folder + elt)
        
    def set_database(self, database): self.__database = database
    def set_logs(self, logs): self.__logs = logs
    
    def fonction(self, cmd: str, args: tuple, author: str):
        returned = None
        if(cmd == 'make_client'): returned = bg.make_client(args[0], args[1], args[2])
        elif(cmd == 'good_login'): returned = bg.good_login(args[0], args[1])
        elif(cmd == 'get_id'): returned = bg.get_id(args[0], args[1])
        elif(cmd == 'make_channel'):
            print('Make Channel by ' + author)
            if(bg.nbr_channel_user(author, author=author) <= 6):
                returned = bg.make_channel(args[0], args[1], author=author)
            else:
                returned = '15'
        elif(cmd == 'join_channel'):
            print('Join Channel by ' + author)
            returned = bg.join_channel(args[2], args[0], args[1])
        elif(cmd == 'name_channel'):
            print('Name Channel activated by ' + author)
            returned = bg.name_channel(args[0])
        elif(cmd == 'get_chat'):
            print('Get Chat activated by ' + author)
            try:
                returned = bg.get_chat(args[0], author=author)
            except: return '-1'
        elif(cmd == 'add_message'): 
            print('Add Message by ' + author)
            if('zajac' in args[1]):
                bg.save_chat(args[0], bg.add_message(args[0], 'Sécurité enfant: ' + str(not self.__kids_securite)))
                self.__kids_securite = not self.__kids_securite
            elif(bg.text_banni(args[1]) and self.__kids_securite): returned = False
            else: returned = bg.save_chat(args[0], bg.add_message(args[0], args[1], author=author))
        elif(cmd == 'clear_chat'):
            if(bg.is_owner(args[0], args[1])):
                print('Clear Chat on the channel ' + args[1] + ' by ' + args[0])
                returned = bg.clear_chat(args[0], args[1])
            else: returned = '9'
        elif(cmd == 'delete_chat'):
            print('Delete chat by ' + author + ' on ' + args[1])
            returned = bg.delete_channel(args[0], args[1])
        elif(cmd == 'is_channel_open'):
            print('Chat is ON ? activated by ' + author)
            returned = bg.is_channel_open(args[0])
            print('Chat ' + str(returned))
        elif(cmd == 'get_id_server'):
            print('Get my server activated by ' + author)
            returned = bg.get_id_server(args[0])
        elif(cmd == 'stop'):
            idd = bg.get_id(author)
            if(idd in self.__owner_account):
                returned = 'stop_all_the_server'
            
        
        return returned
    
    def converte_file(self, name_of_files: str):
        dico = {'return_name': '',
                'author': '',
                'commande': '',
                'args': []}
        
        with open('receive/' + name_of_files, 'r', encoding='UTF-8') as file:
            dico['return_name'] = file.readline()[:-1]
            dico['author'] = file.readline()[:-1]
            temps = file.readline()
            
        command = ''
        args = []
        arg = ''
        x = True
        
        for elt in temps:
            if(x):
                if(elt == '|'): x = False
                else: command += elt
            else:
                if(elt == '/'):
                    args.append(arg)
                    arg = ''
                else:
                    arg += elt
        args.append(arg)
        dico['commande'] = command
        dico['args'] = tuple(args)
        try: os.remove('receive/' + name_of_files)
        except: pass
        return dico
    
    def create_send_file(self, file_name: str, reponse: any):
        try:
            with open('./send/' + file_name , 'a', encoding='UTF-8') as file:
                file.write(str(reponse))
            return True
        except: pass
        
        
    def run(self):
        print('Démarrage du serveur !')
        start = time()
        x = True
        while x:
            now = time()
            if(start + 0.5 < now):
                start = now
                files_getted = os.listdir('receive')
                if(files_getted != []):
                    for files in files_getted:
                        print('Quelques choses de trouvé a ' + str(datetime.now()))
                        dico_file = self.converte_file(files)
                        returned = self.fonction(dico_file['commande'], dico_file['args'], dico_file['author'])
                        if(returned =='stop_all_the_server'): x = False
                        elif(self.create_send_file(dico_file['return_name'], returned)): pass
                        else: print('Erreur avec le fichier ' + dico_file['return_name'])
                        
if __name__ == '__main__' or input('MDP ==> ') == 'bp2022pjt':
    server = Server('db_server.db', True)
    server.run()