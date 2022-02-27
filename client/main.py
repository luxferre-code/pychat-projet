# Main file on client
import pygame, os, sys
import background as bg
from pygame_extension import Button
from time import sleep

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
    auto_connect_file = bg.read_config_file()
    pygame.display.set_caption("PyChat - Login Page")
    login_button = Button('./textures/login_button.png', (1000, 520))
    username_button = Button('./textures/locate_login.png', (largeur // 2 - 700 // 2, hauteur // 3 - 50 // 2))
    
    password_button = Button('./textures/locate_login.png', (largeur // 2 - 700 // 2, hauteur // 3 + 150))
    
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
        username_affiche = font.render(username, True, (0,0,0))
        password_affiche = font.render(affiche_password, True, (0,0,0))
        connexion_auto = pygame.font.Font('./font/UniSansThin.otf', 30).render('Connexion automatique', True, (255, 255, 255))
        screen.blit(username_affiche, (username_button.get_pos()[0], username_button.get_pos()[1] + 17))
        screen.blit(password_affiche, (password_button.get_pos()[0], password_button.get_pos()[1] + 17))
        screen.blit(connexion_auto, (largeur // 20 + 30, hauteur - 70))
        screen.blit(login_button.get_texture(), login_button.get_pos())
        screen.blit(auto_connect.get_texture(), auto_connect.get_pos())
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): sys.exit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                pos_mouse = pygame.mouse.get_pos()
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
                    while True:
                        if(receive_file in os.listdir('./receive')):
                            reponse = bg.get_reponse(receive_file)
                            break
                    auto_connect_file['username'] = username
                    auto_connect_file['password'] = password
                    bg.config_file(auto_connect_file)
                    if(reponse == True):
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
    
def main_page(username: str, password: str):
    pygame.display.set_caption("PyChat - Main Page")
    
    temps_file_name = bg.generate_send_file_name()
    bg.get_id(username, password, temps_file_name)
    while True:
        if(temps_file_name in os.listdir('./receive/')):
            id_user = bg.get_reponse(temps_file_name)
            break
    print(id_user)
    
    pygame.display.set_caption("PyChat - Main Page | ID: " + id_user)
    
    blackway_font = pygame.font.Font('./font/BlackWay.otf', 30)
    welcome_message = blackway_font.render('Welcome, ' + username, True, (255, 255, 255))
    
    while True:
        screen.blit(background, (0, 0))
        screen.blit(welcome_message, (10, 10))
        for events in pygame.event.get():
            if(events.type == pygame.QUIT): sys.exit()
        pygame.display.flip()
    
    
if __name__ == '__main__':
    login_page()