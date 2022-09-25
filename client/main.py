# Main file on client
import pygame, os, sys
import background as bg
from pygame_extension import Button
from time import time

try:
    os.mkdir("send")
except: pass
try:
    os.mkdir("receive")
except: pass

for elt in os.listdir('./receive'):
    os.remove('./receive/' + elt)
for elt in os.listdir('./send'):
    os.remove('./send/' + elt)

# Initialisation de pygame

pygame.init()
largeur, hauteur = taille_fenetre = (1280, 720)
screen = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("PyChat")
pychat_logo = pygame.image.load('./textures/pychat_logo.png')
pygame.display.set_icon(pychat_logo)

# Initialisation des variables

font = pygame.font.Font('./font/UniSansThin.otf', 60)
background = pygame.image.load('./textures/background.png')

if('receive' not in os.listdir()): os.mkdir('receive')
if("send" not in os.listdir()): os.mkdir("send")

def login_page():
    largeur, hauteur = taille_fenetre = (1280, 720)
    screen = pygame.display.set_mode(taille_fenetre)
    
    auto_connect_file = bg.read_config_file()
    pygame.display.set_caption("PyChat - Login Page")
    login_button = Button('./textures/login_button.png', (1000, 520))
    username_button = Button('./textures/locate_login.png', (largeur // 2 - 700 // 2, hauteur // 3 - 50 // 2))
    
    password_button = Button('./textures/locate_login.png', (largeur // 2 - 700 // 2, hauteur // 3 + 150))
    
    no_account = Button('./textures/channel_locate.png', (-125, -50))
    
    pas_de_compte = pygame.font.Font('./font/BlackWay.otf', 45).render('Pas de compte ?', True, (255, 255, 255))
    
    affiche_password = ''
    selected = 'nothing'
    if(auto_connect_file['auto_connect']):
        auto_connect = Button('./textures/cocher.png', (largeur // 20, hauteur - 70))
        username = auto_connect_file['username']
        password = auto_connect_file['password']
    else:
        auto_connect = Button('./textures/pas_cocher.png', (largeur // 20, hauteur - 70))
        username = ''
        password = ''
    while True:
        affiche_password = '*' * len(password)
        screen.blit(background, (0, 0))
        screen.blit(username_button.get_texture(), username_button.get_pos())
        screen.blit(password_button.get_texture(), password_button.get_pos())
        username_affiche = pygame.font.Font('./font/BlackWay.otf', 60).render(username, True, (0,0,0))
        password_affiche = pygame.font.Font('./font/UniSansThin.otf', 60).render(affiche_password, True, (0,0,0))
        connexion_auto = pygame.font.Font('./font/BlackWay.otf', 30).render('Connexion automatique', True, (255, 255, 255))
        screen.blit(username_affiche, (username_button.get_pos()[0], username_button.get_pos()[1] + 17))
        screen.blit(password_affiche, (password_button.get_pos()[0], password_button.get_pos()[1] + 17))
        screen.blit(connexion_auto, (largeur // 20 + 30, hauteur - 70))
        screen.blit(login_button.get_texture(), login_button.get_pos())
        screen.blit(auto_connect.get_texture(), auto_connect.get_pos())
        screen.blit(no_account.get_texture(), no_account.get_pos())
        screen.blit(pas_de_compte, (0, 5))
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): sys.exit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                pos_mouse = pygame.mouse.get_pos()
                if(no_account.is_cliqued(pos_mouse)):
                    create_account()
                if(auto_connect.is_cliqued(pos_mouse)):
                    if(auto_connect.get_texture_dir() == './textures/pas_cocher.png'):
                        auto_connect.change_texture('./textures/cocher.png')
                        auto_connect_file['auto_connect'] = True
                    else:
                        auto_connect.change_texture('./textures/pas_cocher.png')
                        auto_connect_file['auto_connect'] = False
                elif(username_button.is_cliqued(pos_mouse)): selected = 'username_field'
                elif(password_button.is_cliqued(pos_mouse)): selected = 'password_field'
                elif(login_button.is_cliqued(pos_mouse)):
                    receive_file = bg.generate_send_file_name()
                    bg.good_login(username, password, receive_file)
                    # Sender et receiver
                    bg.send_file(receive_file)
                    pygame.time.wait(1500)
                    while not(bg.get_file(receive_file)):
                        print('Rien de trouver !')
                    reponse = bg.get_reponse(receive_file)
                    #
                    auto_connect_file['username'] = username
                    auto_connect_file['password'] = password
                    bg.config_file(auto_connect_file)
                    if(reponse == True):
                        print('Connexion effectué !')
                        main_page(username, password)
                    else:
                        password = ''
                else: selected = 'nothing'
            if(event.type == pygame.KEYDOWN):
                if(selected == 'username_field'):
                    username = bg.text_former(username, event)
                elif(selected == 'password_field'):
                    password = bg.text_former(password, event)
        pygame.display.flip()
        
def channel_creator(id_user: str, username: str, password: str):
    largeur, hauteur = taille_fenetre = (500, 600)
    screen = pygame.display.set_mode(taille_fenetre)
    
    print('Chargement de la fenetre de création de channel !')
    pygame.display.set_caption('PyChat - Channel Creator')
    
    selected = ''
    password = ''
    channels_name = ''
    mdp_activated = Button('./textures/off.png', (400, 200), interne_value=False)
    mdp_button = Button('./textures/channel_locate.png', (50, 275))
    button_name = Button('./textures/channel_locate.png', (50, 75))
    nom_channel = pygame.font.Font('./font/BlackWay.otf', 50).render('Nom du channel:', True, (255, 255, 255))
    mdp_ = pygame.font.Font('./font/BlackWay.otf', 45).render('Mot de passe ?', True, (255,255,255))
    fond_creer = Button('./textures/channel_locate.png', (250, 500))
    creer_text = pygame.font.Font('./font/Blackway.otf', 75).render('Créer !', True, (255, 255, 255))
    
    while True:
        
        name_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render(channels_name, True, (255,255,255))
        pwd_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render(password, True, (255,255,255))
        
        # Affichage sur l'écran
        screen.blit(background, (0, 0))
        screen.blit(mdp_activated.get_texture(), mdp_activated.get_pos())
        screen.blit(button_name.get_texture(), button_name.get_pos())
        screen.blit(nom_channel, (50, 25))
        screen.blit(mdp_, (50, 200))
        screen.blit(fond_creer.get_texture(), fond_creer.get_pos())
        screen.blit(creer_text, (280, 515))
        screen.blit(name_affiche, (button_name.get_pos()[0], button_name.get_pos()[1] + 20))
        if(mdp_activated.get_interne_value()):
            screen.blit(mdp_button.get_texture(), mdp_button.get_pos())
            screen.blit(pwd_affiche, (mdp_button.get_pos()[0], mdp_button.get_pos()[1] + 20))
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                main_page(username, password, auto=True, id_user=id_user)
            if(event.type == pygame.MOUSEBUTTONDOWN):
                pos_mouse = pygame.mouse.get_pos()
                if(button_name.is_cliqued(pos_mouse)): selected = 'button_name'
                elif(mdp_button.is_cliqued(pos_mouse)): selected = 'mdp_button'
                else: selected = ''
                # Mot de passe activé ?
                if(mdp_activated.is_cliqued(pos_mouse)):
                    mdp_activated.set_interne_value(not mdp_activated.get_interne_value())
                    if(mdp_activated.get_interne_value()):
                        mdp_activated.change_texture('./textures/on.png')
                    else:
                        mdp_activated.change_texture('./textures/off.png')
                # Système de création de channel
                if(fond_creer.is_cliqued(pos_mouse)):
                    if(len(channels_name) >= 3 and len(channels_name) <= 12 and ((mdp_activated.get_interne_value() and len(password) > 2) or (not mdp_activated.get_interne_value()))):
                        send = bg.generate_send_file_name()
                        bg.make_channel(channels_name, send, password=password, author=id_user)
                        bg.send_file(send)
                        while not(bg.get_file(send)):
                            print('Rien de trouver !')
                        fait = bg.get_reponse(send)
                        main_page(username, password, auto=True, id_user=id_user)
                    else:
                        print('Impossible de créer le channel !')
            if(event.type == pygame.KEYDOWN):
                if(selected == 'button_name'):
                    channels_name = bg.text_former(channels_name, event)
                elif(selected == 'mdp_button'):
                    password = bg.text_former(password, event)
        pygame.display.flip()
            
    
def main_page(username: str, password: str, auto=False, id_user=''):
    largeur, hauteur = taille_fenetre = (1280, 720)
    screen = pygame.display.set_mode(taille_fenetre)
    
    print('Chargement de la page principale !')
    pygame.display.set_caption("PyChat - Main Page")
    
    if(not auto):
        temps_file_name = bg.generate_send_file_name()
        bg.get_id(username, password, temps_file_name)
        # Sender et receiver
        bg.send_file(temps_file_name)
        while not(bg.get_file(temps_file_name)):
            print('Rien de trouver !')
        id_user = bg.get_reponse(temps_file_name)
        #
    elif(auto and id_user == ''):
        raise ValueError('Erreur PyChat !')
    
    pygame.display.set_caption("PyChat - Main Page | ID: " + id_user)
    
    blackway_font = pygame.font.Font('./font/BlackWay.otf', 30)
    welcome_message = blackway_font.render('Welcome,  ' + username, True, (255, 255, 255))
    logout_button = Button('./textures/logout_button.png', (largeur - 230, 10))
    
    # Créer un channel 08/03/2022
    channel_creator_button = Button('./textures/main_panel_button.png', (25, 150))
    create_channel = pygame.font.Font('./font/BlackWay.otf', 40).render('Créer un salon !', True, (255,255,255))
    
    # Rejoindre un channel 08/03/2022
    join_channel_button = Button('./textures/main_panel_button.png', (25, 250))
    join_channel_text = pygame.font.Font('./font/BlackWay.otf', 40).render('Rejoindre !', True, (255,255,255))
    
    while True:
        screen.blit(background, (0, 0))
        screen.blit(welcome_message, (10, 10))
        screen.blit(logout_button.get_texture(), logout_button.get_pos())
        # Channel creator
        screen.blit(channel_creator_button.get_texture(), channel_creator_button.get_pos())
        screen.blit(create_channel, (channel_creator_button.get_pos()[0] + 7, channel_creator_button.get_pos()[1] + 20))
        # Join channel
        screen.blit(join_channel_button.get_texture(), join_channel_button.get_pos())
        screen.blit(join_channel_text, (join_channel_button.get_pos()[0] + 7, join_channel_button.get_pos()[1] + 20))
        for events in pygame.event.get():
            if(events.type == pygame.QUIT): sys.exit()
            if(events.type == pygame.MOUSEBUTTONDOWN):
                pos_mouse = pygame.mouse.get_pos()
                if(logout_button.is_cliqued(pos_mouse)):
                    del(username)
                    del(password)
                    del(id_user)
                    bg.remove_config_file()
                    login_page()
                elif(channel_creator_button.is_cliqued(pos_mouse)):
                    channel_creator(id_user, username, password)
                elif(join_channel_button.is_cliqued(pos_mouse)):
                    join_channel(username, password, id_user)
        
        
        pygame.display.flip()
        
def join_channel(username, password_user, id_user):
    largeur, hauteur = taille_fenetre = (500, 600)
    screen = pygame.display.set_mode(taille_fenetre)
    
    print('Chargement de la fenetre pour rejoindre un channel !')
    pygame.display.set_caption('PyChat - Join Channel')
    
    selected = ''
    password = ''
    id_channel = ''
    mdp_activated = Button('./textures/off.png', (400, 200), interne_value=False)
    mdp_button = Button('./textures/channel_locate.png', (50, 275))
    button_id = Button('./textures/channel_locate.png', (50, 75))
    id_channel_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render('ID du channel:', True, (255, 255, 255))
    mdp_ = pygame.font.Font('./font/BlackWay.otf', 45).render('Mot de passe ?', True, (255,255,255))
    join_button = Button('./textures/channel_locate.png', (250, 500))
    join = pygame.font.Font('./font/Blackway.otf', 50).render('Rejoindre !', True, (255, 255, 255))
    
    while True:
        name_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render(id_channel, True, (255,255,255))
        pwd_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render(password, True, (255,255,255))
        
        # Affichage sur l'écran
        screen.blit(background, (0, 0))
        screen.blit(mdp_activated.get_texture(), mdp_activated.get_pos())
        screen.blit(button_id.get_texture(), button_id.get_pos())
        screen.blit(id_channel_affiche, (50, 25))
        screen.blit(mdp_, (50, 200))
        screen.blit(join_button.get_texture(), join_button.get_pos())
        screen.blit(join, (280, 515))
        screen.blit(name_affiche, (button_id.get_pos()[0], button_id.get_pos()[1] + 20))
        
        if(mdp_activated.get_interne_value()):
            screen.blit(mdp_button.get_texture(), mdp_button.get_pos())
            screen.blit(pwd_affiche, (mdp_button.get_pos()[0], mdp_button.get_pos()[1] + 20))
        
        for event in pygame.event.get():
            
            #
            if(selected == 'id'): id_channel = bg.text_former(id_channel, event)
            elif(selected == 'pwd'): password = bg.text_former(password, event)
            #
            
            if(event.type == pygame.QUIT): main_page(username, password, auto=True, id_user=id_user)
            
            if(event.type == pygame.MOUSEBUTTONDOWN):
                pos_mouse = pygame.mouse.get_pos()
                if(button_id.is_cliqued(pos_mouse)):
                    selected = 'id'
                elif(mdp_activated.is_cliqued(pos_mouse)):
                    mdp_activated.set_interne_value(not mdp_activated.get_interne_value())
                    
                    if(mdp_activated.get_interne_value()): mdp_activated.change_texture('./textures/on.png')
                    else: mdp_activated.change_texture('./textures/off.png')
                    
                elif(mdp_button.is_cliqued(pos_mouse) and mdp_activated.get_interne_value()):
                    selected = 'pwd'
                elif(join_button.is_cliqued(pos_mouse)):

                    file_name = bg.generate_send_file_name()
                    bg.join_channel(id_channel, password, file_name, author=id_user)
                    bg.send_file(file_name)
                    while not(bg.get_file(file_name)):
                        print('Rien de trouver !')
                    rep = bg.get_reponse(file_name)

                    if(rep):
                        print('Serveur trouvé et connecté avec succés !')
                        chat_panel(username, password_user, id_user, id_channel)
                    else:
                        print('Aucun serveur trouvé avec ces identifiants !')

                else:
                    selected = ''
            
        pygame.display.flip()
        
        
        
        
def chat_panel(username: str, password: str, id_user: str, id_channel: str):
    largeur, hauteur = taille_fenetre = (1280, 720)
    screen = pygame.display.set_mode(taille_fenetre)

    chat_affiche = pygame.image.load('./textures/chat.png')

    send_file = bg.generate_send_file_name()
    bg.name_channel(id_channel, send_file, author=id_user)
    bg.send_file(send_file)

    while not(bg.get_file(send_file)):
        print('Rien de trouver !')
    name_channel = bg.get_reponse(send_file)

    send_file = bg.generate_send_file_name()
    bg.get_chat_channel(id_channel, send_file, author=id_user)
    bg.send_file(send_file)

    while not(bg.get_file(send_file)):
        print('Aucun chat trouvé !')

    all_chat = bg.formater_chat_to_pg(send_file)

    msg = ''

    print('Chargement de la page chat !')
    pygame.display.set_caption("PyChat - Chat Page | ID server: " + id_channel + ' | Channel name: ' + name_channel)

    name_channel_affiche = pygame.font.Font('./font/BlackWay.otf', 35).render('Salon:   ' + name_channel, True, (0,255,125))
    send_button = Button('./textures/send_button.png', (1280 - 85, 720 - 85))
    chat_sender = Button('./textures/chat_sender.png', (1280 - 85 - 820, 720 - 70))

    start = time()
    
    while True:
        msg_affiche = pygame.font.Font('./font/BlackWay.otf', 35).render(msg, True, (255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(name_channel_affiche, (0, 0))
        screen.blit(chat_affiche, (largeur - 800 - 20, hauteur - 600 - 90))
        screen.blit(chat_sender.get_texture(), chat_sender.get_pos())
        screen.blit(send_button.get_texture(), send_button.get_pos())
        screen.blit(msg_affiche, (chat_sender.get_pos()[0] + 3, chat_sender.get_pos()[1] + 10))

        for k in range(len(all_chat)):
            screen.blit(all_chat[k], (largeur - 800 - 10, hauteur - 600 - 90 + (30 * k)))

        if(time() - start > 3):
            start = time()

            send_file = bg.generate_send_file_name()
            bg.get_chat_channel(id_channel, send_file, author=id_user)
            bg.send_file(send_file)

            while not(bg.get_file(send_file)):
                print('Aucun chat trouvé !')

            all_chat = bg.formater_chat_to_pg(send_file)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT): sys.exit()
            if(event.type == pygame.KEYDOWN): msg = bg.text_former(msg, event)
            if(event.type == pygame.MOUSEBUTTONDOWN):
                pos_mouse = pygame.mouse.get_pos()
                if(send_button.is_cliqued(pos_mouse)):
                    send_file = bg.generate_send_file_name()
                    bg.add_message(msg, id_channel, send_file, author=id_user)
                    bg.send_file(send_file)
                    msg = ''

                    start = time()

                    send_file = bg.generate_send_file_name()
                    bg.get_chat_channel(id_channel, send_file, author=id_user)
                    bg.send_file(send_file)

                    while not(bg.get_file(send_file)):
                        print('Aucun chat trouvé !')

                    all_chat = bg.formater_chat_to_pg(send_file)


        pygame.display.flip()
        
    
    
    
def create_account():
    pygame.display.set_caption('PyChat - Create Account')
    username = ''
    password = ''
    confirm_pwd = ''
    mail = ''
    selected = ''
    
    
    mdp_activated = Button('./textures/off.png', (550, 250), interne_value=False)
    confirm_mdp_activated = Button('./textures/off.png', (550, 350), interne_value=False)
    username_field = Button('./textures/button_c_acc.png', (50, 100))
    password_field = Button('./textures/button_c_acc.png', (50, 250))
    confirm_pwd_field = Button('./textures/button_c_acc.png', (50, 350))
    mail_field = Button('./textures/button_c_acc.png', (50, 500))
    create_account = Button('./textures/create_account.png', (900, 520))
    create_account_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render("create account", True, (255, 255, 255))
    username_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render("enter username", True, (255,255,255))
    password_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render("enter password", True, (255,255,255))
    confirm_pwd_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render("confirm password", True, (255,255,255))
    mail_affiche = pygame.font.Font('./font/BlackWay.otf', 50).render("enter mail", True, (255,255,255))
    while True:
        screen.blit(background, (0, 0))
        screen.blit(create_account.get_texture(), create_account.get_pos())
        screen.blit(create_account_affiche, (create_account.get_pos()[0], create_account.get_pos()[1] + 35))
        screen.blit(username_field.get_texture(), username_field.get_pos()) 
        if selected != 'username_field' and username == '': screen.blit(username_affiche, (username_field.get_pos()[0]+ 120, username_field.get_pos()[1] + 18))
        screen.blit(password_field.get_texture(), password_field.get_pos()) 
        if selected != 'password_field' and password == '': screen.blit(password_affiche, (password_field.get_pos()[0]+ 120, password_field.get_pos()[1] + 18))
        screen.blit(confirm_pwd_field.get_texture(), confirm_pwd_field.get_pos()) 
        if selected != 'confirm_pwd_field' and confirm_pwd == '': screen.blit(confirm_pwd_affiche, (confirm_pwd_field.get_pos()[0]+ 100, confirm_pwd_field.get_pos()[1] + 18))
        screen.blit(mail_field.get_texture(), mail_field.get_pos()) 
        if selected != 'mail_field' and mail == '': screen.blit(mail_affiche, (mail_field.get_pos()[0]+ 150, mail_field.get_pos()[1] + 18))
        screen.blit(pygame.font.Font('./font/BlackWay.otf', 50).render(username, True, (255,255,255)),(50, 100))
        screen.blit(pygame.font.Font('./font/BlackWay.otf', 50).render(mail, True, (255,255,255)),(50,500))
        screen.blit(mdp_activated.get_texture(), mdp_activated.get_pos())
        screen.blit(confirm_mdp_activated.get_texture(), confirm_mdp_activated.get_pos())

        if(mdp_activated.get_interne_value()): screen.blit(pygame.font.Font('./font/BlackWay.otf', 50).render(password, True, (255,255,255)),(50, 250))
        else: screen.blit(pygame.font.Font('./font/UniSansThin.otf', 65).render('*' * len(confirm_pwd), True, (255,255,255)),(50,370))

        if(confirm_mdp_activated.get_interne_value()): screen.blit(pygame.font.Font('./font/BlackWay.otf', 50).render(confirm_pwd, True, (255,255,255)),(50,350))
        else: screen.blit(pygame.font.Font('./font/UniSansThin.otf', 65).render('*' * len(password), True, (255,255,255)),(50, 270))
            
       
        
        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN):
                
                
                if selected == 'username_field':
                    username = bg.text_former(username, event)
              
                if selected == 'password_field':
                    password = bg.text_former(password, event)
                
                if selected == 'confirm_pwd_field':
                    confirm_pwd = bg.text_former(confirm_pwd, event)
                
                if selected == 'mail_field':
                    mail = bg.text_former(mail, event)
            if(event.type == pygame.QUIT): sys.exit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                
                pos_mouse = pygame.mouse.get_pos()
                if(mdp_activated.is_cliqued(pos_mouse)):
                    mdp_activated.set_interne_value(not mdp_activated.get_interne_value())
                    if(mdp_activated.get_interne_value()):
                        mdp_activated.change_texture('./textures/on.png')
                    else:
                        mdp_activated.change_texture('./textures/off.png')
                if(confirm_mdp_activated.is_cliqued(pos_mouse)):
                    confirm_mdp_activated.set_interne_value(not confirm_mdp_activated.get_interne_value())
                    if(confirm_mdp_activated.get_interne_value()):
                        confirm_mdp_activated.change_texture('./textures/on.png')
                    else:
                        confirm_mdp_activated.change_texture('./textures/off.png')
                if(create_account.is_cliqued(pos_mouse)):
                    if(len(username) >= 3 and len(username) <= 12) and (len(password) != 0) and ("@" in mail) and confirm_pwd == password:
                        receive_file = bg.generate_send_file_name()
                        bg.make_client(username, mail, password, receive_file)
                        bg.send_file(receive_file)
                        while not(bg.get_file(receive_file)):
                            print('Rien de trouver !')
                        reponse = bg.get_reponse(receive_file)
                        if reponse: login_page()
                    else:
                        username = ''
                        password = ''
                        mail = ''


                if(username_field.is_cliqued(pos_mouse)):
                    selected = 'username_field'
                elif(password_field.is_cliqued(pos_mouse)):
                    selected = 'password_field'
                elif(confirm_pwd_field.is_cliqued(pos_mouse)):
                    selected = 'confirm_pwd_field'
                elif(mail_field.is_cliqued(pos_mouse)):
                    selected = 'mail_field'
                        
                        
       
                        
                    
                
        #print(username_field.is_cliqued(pos_mouse))
        pygame.display.flip()
    
if __name__ == '__main__' and True:
    #join_channel('@Console', 'root', '0000000000')
    #channel_creator('0000000000', '@Console', 'root')
    #chat_panel('Valentin', '', '0000000000', '1234567890')
    login_page()
