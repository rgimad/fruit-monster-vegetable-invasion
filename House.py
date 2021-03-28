import pygame
from pygame.locals import (
    RLEACCEL,
)

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(House, self).__init__()
        self.block_type = block_type
        for i in range(0, 10):
            if block_type == str(i):
                st = "assets/images/house/house" + str(i) + ".png"
                self.surf = pygame.image.load(st)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, House deleted.')