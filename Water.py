import pygame
from pygame.locals import (
    RLEACCEL,
)
from const import PATH_IMG_WATER3, PATH_IMG_WATER4

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(Water, self).__init__()
        self.block_type = block_type
        if block_type == 'W':
            self.surf = pygame.image.load(PATH_IMG_WATER3)
        elif block_type == 'H':
            self.surf = pygame.image.load(PATH_IMG_WATER4)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, Water deleted.')