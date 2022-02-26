# Main file on client
import pygame, os, sys
import background as bg
from pygame_extension import Button

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
    pygame.display.set_caption("PyChat - Login Page")
    login_button = Button('./textures/login_button.png', (1000, 520))
    username_button = Button('./textures/locate_login.png', (largeur // 2 - 700 // 2, hauteur // 3 - 50 // 2))
    username = ''
    password_button = Button('./textures/locate_login.png', (largeur // 2 - 700 // 2, hauteur // 3 + 150))
    password = ''
    affiche_password = ''
    selected = 'nothing'
    while True:
        affiche_password = '*' * len(password)
        screen.blit(background, (0, 0))
        screen.blit(username_button.get_texture(), username_button.get_pos())
        screen.blit(password_button.get_texture(), password_button.get_pos())
        username_affiche = font.render(username, True, (0,0,0))
        password_affiche = font.render(affiche_password, True, (0,0,0))
        screen.blit(username_affiche, (username_button.get_pos()[0], username_button.get_pos()[1] + 17))
        screen.blit(password_affiche, (password_button.get_pos()[0], password_button.get_pos()[1] + 17))
        screen.blit(login_button.get_texture(), login_button.get_pos())
        for event in pygame.event.get():
            if(event.type == pygame.QUIT): sys.exit()
            if(event.type == pygame.MOUSEBUTTONDOWN):
                pos_mouse = pygame.mouse.get_pos()
                if(username_button.is_cliqued(pos_mouse)): selected = 'username_field'
                elif(password_button.is_cliqued(pos_mouse)): selected = 'password_field'
                elif(login_button.is_cliqued(pos_mouse)):
                    print("Username: " + username + "\nPassword: " + bg.to_sha256(password))
                    receive_file = bg.generate_send_file_name()
                    bg.good_login(username, password, receive_file)
                else: selected = 'nothing'
            if(event.type == pygame.KEYDOWN):
                if(selected == 'username_field'):
                    username = bg.text_former(username, event)
                elif(selected == 'password_field'):
                    password = bg.text_former(password, event)
        pygame.display.flip()
    
login_page()