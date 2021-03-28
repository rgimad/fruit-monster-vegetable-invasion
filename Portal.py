import pygame
from pygame.locals import (
    RLEACCEL,
)
from const import PATH_IMG_PORTAL1

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type = 1):
        super(Portal, self).__init__()
        self.block_type = block_type
        self.surf = pygame.image.load(PATH_IMG_PORTAL1).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, Portal deleted.')