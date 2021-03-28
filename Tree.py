import pygame
from pygame.locals import (
    RLEACCEL,
)
from const import (
    PATH_IMG_TREE1,
    PATH_IMG_TREE2,
    PATH_IMG_TREE3,
    PATH_IMG_TREE4,
    PATH_IMG_TREE11,
    PATH_IMG_TREE12,
    PATH_IMG_TREE13,
    PATH_IMG_TREE14,
    PATH_IMG_TREE21,
    PATH_IMG_TREE22,
    PATH_IMG_TREE23,
    PATH_IMG_TREE24,
)

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(Tree, self).__init__()
        self.block_type = block_type
        if block_type == 'T':
            self.surf = pygame.image.load(PATH_IMG_TREE1)
        elif block_type == 'O':
            self.surf = pygame.image.load(PATH_IMG_TREE2)
        elif block_type == 'X':
            self.surf = pygame.image.load(PATH_IMG_TREE3)
        elif block_type == 'A':
            self.surf = pygame.image.load(PATH_IMG_TREE4)
        elif block_type == 't':
            self.surf = pygame.image.load(PATH_IMG_TREE11)
        elif block_type == 'o':
            self.surf = pygame.image.load(PATH_IMG_TREE12)
        elif block_type == 'x':
            self.surf = pygame.image.load(PATH_IMG_TREE13)
        elif block_type == 'a':
            self.surf = pygame.image.load(PATH_IMG_TREE14)
        elif block_type == 'l':
            self.surf = pygame.image.load(PATH_IMG_TREE21)  
        elif block_type == 'k':
            self.surf = pygame.image.load(PATH_IMG_TREE22) 
        elif block_type == 'j':
            self.surf = pygame.image.load(PATH_IMG_TREE23) 
        elif block_type == 'u':
            self.surf = pygame.image.load(PATH_IMG_TREE24)               
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))        

    def __del__(self):
        pass
        # print('Destructor called, Tree deleted.')