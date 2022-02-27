import pygame
from PIL import Image

class Button:
    def __init__(self, texture_dir: str, pos: tuple) -> None:
        self.__x, self.__y = self.__pos = pos
        self.__dir_tex = texture_dir
        self.__texture = pygame.image.load(texture_dir)
        
    def get_x(self): return self.__x
    def get_y(self): return self.__y
    def get_pos(self): return self.__pos
    def get_texture_dir(self): return self.__dir_tex
    def get_texture(self): return self.__texture
    
    def change_texture(self, texture_dir: str):
        self.__dir_tex = texture_dir
        self.__texture = pygame.image.load(texture_dir)
    
    def change_pos(self, new_pos: tuple) -> bool:
        assert isinstance(new_pos, tuple) or isinstance(new_pos, list), "Les positions doit être soit un tuple soit une liste"
        assert len(new_pos) == 2, "new_pos doit contenir deux coordonnées (x/y)"
        try:
            self.__x, self.__y = self.__pos = new_pos
            return True
        except:
            return False
        
    def is_cliqued(self, pos_mouse: tuple) -> bool:
        assert isinstance(pos_mouse, tuple) or isinstance(pos_mouse, list), "Les positions doit être soit un tuple soit une liste"
        assert len(pos_mouse) == 2, "pos_mouse doit contenir deux coordonnées (x/y)"
        width, height = Image.open(self.__dir_tex).width, Image.open(self.__dir_tex).height
        larg_mouse, haut_mouse = pos_mouse
        if(larg_mouse >= self.__x and larg_mouse <= self.__x + width and haut_mouse >= self.__y and haut_mouse <= self.__y + height): return True
        else: return False