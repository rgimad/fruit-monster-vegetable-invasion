import pygame
from pygame.locals import (
    RLEACCEL,
)

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type):
        super(Tree, self).__init__()
        self.block_type = block_type
        if block_type == 'T':
            self.surf = pygame.image.load("assets/images/tree/tree1.png") 
        elif block_type == 'O':
            self.surf = pygame.image.load("assets/images/tree/tree2.png") 
        elif block_type == 'X':
            self.surf = pygame.image.load("assets/images/tree/tree3.png") 
        elif block_type == 'A':
            self.surf = pygame.image.load("assets/images/tree/tree4.png")     
        elif block_type == 't':
            self.surf = pygame.image.load("assets/images/tree/tree11.png") 
        elif block_type == 'o':
            self.surf = pygame.image.load("assets/images/tree/tree12.png") 
        elif block_type == 'x':
            self.surf = pygame.image.load("assets/images/tree/tree13.png") 
        elif block_type == 'a':
            self.surf = pygame.image.load("assets/images/tree/tree14.png")               
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))        

    def __del__(self):
        pass
        # print('Destructor called, Tree deleted.')