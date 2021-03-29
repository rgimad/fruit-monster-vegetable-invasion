import pygame
from pygame.locals import (
    RLEACCEL,
)

from const import PATH_IMG_STONE1, PATH_IMG_BRICK2, PATH_IMG_BOX, \
     PATH_IMG_ICE, PATH_IMG_WERT_WALL, PATH_IMG_HOR_WALL, \
         PATH_IMG_ANGLE_LEFT_UP_WALL, PATH_IMG_ANGLE_RIGHT_UP_WALL, \
             PATH_IMG_ANGLE_LEFT_DOWN_WALL, PATH_IMG_ANGLE_RIGHT_DOWN_WALL, \
                 PATH_IMG_TEXTURE_MOB, PATH_IMG_TEXTURE_MOB_DOWN, PATH_IMG_TEXTURE_MOB_RIGHT, \
                     PATH_IMG_TEXTURE_MOB_UP
             

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(Brick, self).__init__()
        self.block_type = block_type
        if block_type == '#':
            self.surf = pygame.image.load(PATH_IMG_STONE1).convert()
        elif block_type == '$':
            self.surf = pygame.image.load(PATH_IMG_BRICK2).convert()
        elif block_type == 'B':
            self.surf = pygame.image.load(PATH_IMG_BOX).convert()
        elif block_type == 'q':
            self.surf = pygame.image.load(PATH_IMG_ICE).convert()
        elif block_type == '*':
            self.surf = pygame.image.load(PATH_IMG_WERT_WALL).convert()
        elif block_type == '&':
            self.surf = pygame.image.load(PATH_IMG_HOR_WALL).convert()
        elif block_type == '<':
            self.surf = pygame.image.load(PATH_IMG_ANGLE_LEFT_UP_WALL).convert()
        elif block_type == '>':
            self.surf = pygame.image.load(PATH_IMG_ANGLE_RIGHT_UP_WALL).convert()
        elif block_type == '{':
            self.surf = pygame.image.load(PATH_IMG_ANGLE_LEFT_DOWN_WALL).convert()
        elif block_type == '}':
            self.surf = pygame.image.load(PATH_IMG_ANGLE_RIGHT_DOWN_WALL).convert()
        elif block_type == '?':
            self.surf = pygame.image.load(PATH_IMG_TEXTURE_MOB).convert()
        elif block_type == ';':
            self.surf = pygame.image.load(PATH_IMG_TEXTURE_MOB_DOWN).convert()
        elif block_type == '^':
            self.surf = pygame.image.load(PATH_IMG_TEXTURE_MOB_UP).convert()
        elif block_type == '-':
            self.surf = pygame.image.load(PATH_IMG_TEXTURE_MOB_RIGHT).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, Brick deleted.')