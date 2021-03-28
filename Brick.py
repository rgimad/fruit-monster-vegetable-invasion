import pygame
from pygame.locals import (
    RLEACCEL,
)

from const import PATH_IMG_STONE1, PATH_IMG_BRICK2, PATH_IMG_BOX, PATH_IMG_ICE

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
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, Brick deleted.')