import pygame
from pygame.locals import (
    RLEACCEL,
)

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(Brick, self).__init__()
        self.block_type = block_type
        if block_type == '#':
            self.surf = pygame.image.load("assets/images/stone1.png").convert()
        elif block_type == '$':
            self.surf = pygame.image.load("assets/images/brick2.png").convert()
        elif block_type == 'B':
            self.surf = pygame.image.load("assets/images/box.png").convert()     
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, Brick deleted.')