import sys
import math
import pygame
import random as rd

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_a,
    K_s,
    K_d,
    KEYDOWN,
    QUIT,
)
class Menu:
    def __init__(self, punkts):
        self.punkts = punkts

    def render(self, screen, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                screen.blit(font.render(i[2], 2, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 2, i[3]), (i[0], i[1]))
    def menu(self):
        done = True
        self.menu_back = pygame.image.load('assets/images/background1.jpg')
        pygame.init()
        pygame.mixer.music.load('assets/sounds/menu.mp3')
        pygame.mixer.music.play(loops=-1)


        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)
        punkt = None
        while done:
            screen.blit(self.menu_back, (0, 0))
            mp = pygame.mouse.get_pos()
            self.render(screen, font_menu, punkt)
            
        
            for i in self.punkts:
                if mp[0]>=i[0] and mp[0]<i[0]+130 and mp[1]>=i[1]-150 and mp[1]<i[1]-100:
                    punkt = 0
                elif  mp[0]>=i[0] and mp[0]<i[0]+330 and mp[1]>=i[1]-40 and mp[1]<i[1]-20:
                    punkt = 1  
                elif mp[0]>=i[0] and mp[0]<i[0]+110 and mp[1]>=i[1] and mp[1]<i[1]+100:
                    punkt = 2   
                else :
                    punkt= None
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                       sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 :
                         if punkt == 0:
                             self.game1 = Game()
                             self.game1.main()  
                         elif punkt == 2:
                               exit()
     
            window.blit(screen, (0, 30))
            pygame.display.flip()

class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Mob, self).__init__()
        self.game = game
        self.surf = pygame.image.load("assets/images/mob1.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.mobRandomSpawnOnX = (70, 140, 210, 1000, 444, 555, 666)
        self.mobRandomSpawnOnY = (70, 140, 210, 1000, 666, 444, 555)
        print(rd.choice(self.mobRandomSpawnOnX), rd.choice(self.mobRandomSpawnOnY))
        self.rect = self.surf.get_rect(topleft = (rd.choice(self.mobRandomSpawnOnX), rd.choice(self.mobRandomSpawnOnY)))
        #self.rect = self.surf.get_rect(topleft = (self.game.SCREEN_WIDTH / 7, self.game.SCREEN_HEIGHT / 7))
        self.dir_x = 0
        self.dir_y = 0

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game # reference to Game object in which player is playing
        #self.surf = pygame.Surface((75, 75))
        #self.surf.fill((255, 255, 255))
        self.surf = pygame.image.load("assets/images/bear2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # create rect from surface and set initial coords (by default they;re (0, 0
        self.rect = self.surf.get_rect(topleft = (self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2))
        self.dir_x = 0
        self.dir_y = 1
        

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        dx, dy = 0, 0
        if pressed_keys[K_UP]:# or pressed_keys[K_w]:
            #dx, dy = 0, -5
            #dy -= 5
            self.rect.move_ip(0, -5)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:# or pressed_keys[K_s]:
            #dx, dy = 0, 5
            #dy += 5
            self.rect.move_ip(0, 5)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:# or pressed_keys[K_a]:
            #dx, dy = -5, 0
            #dx -= 5
            self.rect.move_ip(-5, 0)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:# or pressed_keys[K_d]:
            #dx, dy = 5, 0
            #dx += 5
            self.rect.move_ip(5, 0)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(-5, 0)

        #self.rect.move_ip(dx, dy)
        #if pygame.sprite.spritecollideany(self, self.game.bricks):
        #    self.rect.move_ip(-dx, -dy)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.SCREEN_WIDTH:
            self.rect.right = self.game.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.game.SCREEN_HEIGHT:
            self.rect.bottom = self.game.SCREEN_HEIGHT

class Map():
    def __init__(self):
        self.rows = None
        self.cols = None
        self.path = None
        self.matrix = None
        self.cell_size = 72

    def load_from(self, filepath = 'assets/maps/map1.txt'):
        self.path = filepath
        f = open(filepath)
        self.matrix = f.read().split('\n')
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def cell(self, row, col):
        return self.matrix[row][col]        


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Brick, self).__init__()
        self.surf = pygame.image.load("assets/images/brick1.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

class TerrainBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type = 1):
        super(TerrainBlock, self).__init__()
        self.surf = pygame.image.load("assets/images/terrain1.png" if block_type == 1 else "assets/images/terrain2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))

class Game():
    def __init__(self):
        surface = pygame.display.get_surface()
        self.SCREEN_WIDTH,self.SCREEN_HEIGHT = size = surface.get_width(), surface.get_height()
        self.FPS = 60
        self.map = Map()
        self.map.load_from('assets/maps/map1.txt')
        self.running = False
        
        pygame.init()

        #info_object = pygame.display.Info()
        #self.SCREEN_WIDTH, self.SCREEN_HEIGHT = info_object.current_w, info_object.current_h
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT) ) #, flags = pygame.FULLSCREEN )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        self.player = Player(self) # create a player
        # trying to create an array of objects in class Mob
        self.listMob = []
        for i in range(10):
            self.listMob.append(Mob(i))

        self.bricks = pygame.sprite.Group()
        self.terrain_blocks = pygame.sprite.Group()

    def draw_map(self):
        for i in range(self.map.rows):
            for j in range(self.map.cols):
                cell = self.map.cell(i, j)
                if cell == '#':
                    new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size)
                    self.bricks.add(new_brick)
                elif cell == '.':
                    new_terrain_block = TerrainBlock(j*self.map.cell_size, i*self.map.cell_size)
                    self.terrain_blocks.add(new_terrain_block)
                else:
                    print('map error: incorrect cell type')
                    

    def main(self):
        pygame.mixer.music.load('assets/sounds/music1.mp3')
        pygame.mixer.music.play(loops=-1)
        self.running = True # flag that show is game running or not
        pygame.event.set_grab(True)

        self.draw_map()
        while self.running:
            self.clock.tick(self.FPS)  # delay according to fps
            
            for event in pygame.event.get(): # check events
                
                if event.type == KEYDOWN:         # when user hits some button
                    if event.key == K_ESCAPE:     # Esc -> quit
                        self.running = False

                elif event.type == pygame.MOUSEMOTION:
                    m_x, m_y = event.pos
                    l = math.sqrt((m_x - self.player.rect.x)**2 + (m_y - self.player.rect.y)**2)
                    if l > 0:
                        self.player.dir_x = (m_x - self.player.rect.x) / l
                        self.player.dir_y = (m_y - self.player.rect.y) / l
                    
                        
                elif event.type == pygame.QUIT:   # if user closes the widow -> quit
                    self.running = False

                #else:
                #    print(event.type, pygame.mouse.get_pos())

            # Get all the keys currently pressed
            pressed_keys = pygame.key.get_pressed()

            # Update the player sprite based on user keypresses
            self.player.update(pressed_keys)

            #self.screen.fill((0, 0, 0))
            

            for entity in self.terrain_blocks:
                self.screen.blit(entity.surf, entity.rect)

            for entity in self.bricks:
                self.screen.blit(entity.surf, entity.rect)

            # Draw the player on the screen
            self.screen.blit(self.player.surf, self.player.rect)
            for i in range(10):
                self.screen.blit(self.listMob[i].surf, self.listMob[i].rect)

            pygame.draw.line(self.screen, (0, 30, 225), 
                     [self.player.rect.x, self.player.rect.y], 
                     [self.player.rect.x + 700*self.player.dir_x, self.player.rect.y + 700*self.player.dir_y], 2)

            # draw fps ounter
            fps = self.font.render('FPS: ' + str(int(self.clock.get_fps())), True, pygame.Color('white'))
            self.screen.blit(fps, (50, 30))

            # update the display
            pygame.display.flip()

        pygame.quit()
        sys.exit()

pygame.font.init()                   
punkts = [(1000, 520, u'Играть', (11, 0, 77), (250,250,30), 0),
          (1000, 610, u'Выбор персонажа', (11, 0, 77), (250,250,30), 1),
          (1000, 700, u'Выйти', (11, 0, 77), (250,250,30), 2)]

if __name__ == "__main__":
    game = Menu(punkts)
    game.menu()
