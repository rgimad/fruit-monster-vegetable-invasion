import pygame
from pygame.locals import (
    RLEACCEL,
)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(Door, self).__init__()
        self.block_type = block_type
        if block_type == 'D':
            self.surf = pygame.image.load("assets/images/open_door1.png").convert()
        elif block_type == 'd':
            self.surf = pygame.image.load("assets/images/open_door2.png").convert()
        else:
            self.surf = pygame.image.load("assets/images/closed_door.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, Door deleted.')