import pygame
from pygame.locals import (
    RLEACCEL,
)
from const import PATH_IMG_SECRET_TERR_BLOCK

class TerrainBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type = 1, index_level = 1):
        super(TerrainBlock, self).__init__()
        self.block_type = block_type
        if self.block_type == ':':
            self.surf = pygame.image.load(PATH_IMG_SECRET_TERR_BLOCK).convert()
        else:
            self.surf = pygame.image.load("assets/images/gross" + str(index_level) + ".png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

    def __del__(self):
        pass
        # print('Destructor called, TerrBlock deleted.')