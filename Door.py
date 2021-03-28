import pygame
from pygame.locals import (
    RLEACCEL,
)
from const import PATH_IMG_OPEN_DOOR1, PATH_IMG_OPEN_DOOR2, PATH_IMG_CLOSED_DOOR

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(Door, self).__init__()
        self.block_type = block_type
        if block_type == 'D':
            self.surf = pygame.image.load(PATH_IMG_OPEN_DOOR1).convert()
        elif block_type == 'd':
            self.surf = pygame.image.load(PATH_IMG_OPEN_DOOR2).convert()
        else:
            self.surf = pygame.image.load(PATH_IMG_CLOSED_DOOR).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, Door deleted.')