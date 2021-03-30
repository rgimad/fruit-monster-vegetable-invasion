import sys
import os
import math
import pygame
import threading
import time
import numpy as np
from random import shuffle
import LeeMovement as lee
import random as rd
import PIL
from PIL import Image

from const import *

from Brick import Brick
from TerrainBlock import TerrainBlock
from House import House
from Tree import Tree
from Water import Water
from Portal import Portal
from Door import Door

index_level = 1 # change the current level
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info_object = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info_object.current_w, info_object.current_h
constx, consty = SCREEN_WIDTH / 1366, SCREEN_HEIGHT / 768
consth = 1.00682012 if constx == 1 else 1

if not os.path.exists('save'):
    os.makedirs('save')

pygame.init()
shoot_sound = pygame.mixer.Sound(PATH_SND_SHOOT3)
shoot_sound.set_volume(0.1)

damage_sound = []
for snd in [PATH_SND_DAMAGE1, PATH_SND_DAMAGE2]:
    damage_sound.append(pygame.mixer.Sound(snd))

rev_sound = pygame.mixer.Sound(PATH_SND_REV)
rev_sound.set_volume(1.5)

boss_sound = pygame.mixer.Sound(PATH_SND_BOSS)
boss_sound.set_volume(1.5)

collision_sound = pygame.mixer.Sound(PATH_SND_COLLISION)

buulet_to_brick_sound = pygame.mixer.Sound(PATH_SND_BULLET_TO_BRICK)

notshoot_sound = pygame.mixer.Sound(PATH_SND_NOTSHOOT)
reload_sound = pygame.mixer.Sound(PATH_SND_RELOAD)
portal_sound = pygame.mixer.Sound(PATH_SND_PORTAL)

from pygame.locals import ( RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE,
    K_w, K_a, K_s, K_d, KEYDOWN, QUIT, K_SPACE, K_m, K_n, K_r, )

class Menu:
    def __init__(self):
        self.menu_point = None
        self.isFirstMenu = True
        self.isChangeLevel = False
        self.isInfo = False
        self.constPixel = 0
        self.back_menu = self.get_resize_image('background3', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.level = [0, 0, 0, 0, 0]
        for i in range(5):
            self.level[i] = self.get_resize_image('level'+ str(i + 1), math.ceil(214*constx), math.ceil(357*consty)) 
        self.block_level = self.get_resize_image('block_level1', math.ceil(214*constx), math.ceil(357*consty))
        self.loading = self.get_resize_image('loading', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.back_info = self.get_resize_image('back_info', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.points_in_first_menu = [
            (1070*constx, 600*consty, u'Играть', (250, 97, 3), (255, 165, 0), 0),
            (1070*constx, 660*consty, u'Управление', (250, 97, 3), (255, 165, 0), 1),
            (1070*constx, 720*consty, u'Выйти', (250, 97, 3), (255, 165, 0),  2)
        ]
        self.points_in_second_menu = [
            (1070*constx, 600*consty, u'Новая игра', (250, 97, 3), (255, 165, 0), 0),
            (1070*constx, 660*consty, u'Выбрать уровень', (250, 97, 3), (255, 165, 0), 1),
            (1070*constx, 720*consty, u'Назад', (250, 97, 3), (255, 165, 0),  2)
        ]
        self.backInChoiceLvl = [(1070*constx, 720*consty, u'Назад', (250, 97, 3), (255, 165, 0),  2)]

    def __del__(self):
        pass
        # print('Destructor called, Menu deleted.')

    def render(self, screen, font, points, num_punkt):
        for i in points:
            if num_punkt == i[5]:
                screen.blit(font.render(i[2], 2, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 2, i[3]), (i[0], i[1]))

    def get_menu_point(self, mp, points):
        for i in points:
            if mp[0]>=i[0] and mp[0]<i[0]+180 and mp[1]>=i[1]-125*consty and mp[1]<i[1]-100*consty:
                self.menu_point = 0
            elif  mp[0]>=i[0] and mp[0]<i[0]+300 and mp[1]>=i[1]-65*consty and mp[1]<i[1]-40*consty:
                self.menu_point = 1  
            elif mp[0]>=i[0] and mp[0]<i[0]+110 and mp[1]>=i[1] and mp[1]<i[1]+100*consty:
                self.menu_point = 2   
            else:
                self.menu_point = None
                
    def in_first_menu(self, e, mp):
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.menu_point == 0:
                self.isFirstMenu = False
            elif self.menu_point == 1:
                self.isFirstMenu = False
                self.isInfo = True
                self.back_menu = pygame.image.load('assets/images/Resize/back_infoResize.png')
            elif self.menu_point == 2:
                sys.exit()
    
    def in_second_menu(self, e, mp):
        global index_level
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.isFirstMenu = True
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.menu_point == 0:
                pygame.image.load(PATH_IMG_RESIZE_LOADING)
                index_level = 1
                l = open(PATH_SAVE_OPEN_LVL,'w') 
                l.write(str(1))
                l.close()
                max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'w')
                max_f.write(str(1))
                max_f.close()
                time.sleep(1)
                self.game = Game()
                self.game.main()
                self.choose_next_level()
            elif self.menu_point == 1:
                self.isChangeLevel = True
                self.back_menu = self.get_resize_image('back_lvl', SCREEN_WIDTH, SCREEN_HEIGHT)
            elif self.menu_point == 2:
                self.isFirstMenu = True

    def menu_info(self, e, mp):
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.back_menu = pygame.image.load('assets/images/Resize/background3Resize.png')
                self.isFirstMenu = True
                self.isInfo = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
            if self.menu_point == 2:
                self.back_menu = pygame.image.load('assets/images/Resize/background3Resize.png')
                self.isFirstMenu = True
                self.isInfo = False

    def choose_next_level(self):
        global index_level
        pygame.image.load(PATH_IMG_RESIZE_LOADING)
        r = open(PATH_SAVE_OPEN_LVL, 'r')
        tmp = int(r.readline())
        if tmp != index_level:
            index_level = tmp
            self.game = Game()
            self.game.main()
            return self.choose_next_level()

    def choose_user_level(self):
        try:
            max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'r')
        except:
            max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'w+')
            max_f.write('1')
            max_f.flush()
            max_f.seek(0)
        max_opened_level = int(max_f.readline())
        max_f.close()
        l = open(PATH_SAVE_OPEN_LVL,'w')
        l.write(str(index_level))
        l.close()
        b = open("save/bonus_after_"+ str(index_level + 1) +"_lvl.txt",'w') 
        b.write("0")
        b.close()
        if max_opened_level >= index_level:
            self.game = Game()
            self.game.main()
            return self.choose_next_level()

    def in_choise_lvl_menu(self, e, mp):
        global index_level
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.back_menu = pygame.image.load('assets/images/Resize/background3Resize.png')
                self.isChangeLevel = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
            if mp[0]>86*constx and mp[0]<321*constx and mp[1]>290*consty and mp[1]<633*consty:
                index_level = 1
                self.choose_user_level()
            elif mp[0]>365*constx and mp[0]<571*constx and mp[1]>290*consty and mp[1]<633*consty:
                index_level = 2
                self.choose_user_level()
            elif mp[0]>=601*constx and mp[0]<803*constx and mp[1]>290*consty and mp[1]<633*consty:
                index_level = 3
                self.choose_user_level()
            elif mp[0]>=841*constx and mp[0]<1032*constx and mp[1]>290*consty and mp[1]<633*consty:
                index_level = 4
                self.choose_user_level()
            elif mp[0]>=1075*constx and mp[0]<1270*constx and mp[1]>290*consty and mp[1]<633*consty:
                index_level = 5
                self.choose_user_level()
            elif self.menu_point == 2:
                self.back_menu = pygame.image.load('assets/images/Resize/background3Resize.png')
                self.isChangeLevel = False
    
    def get_resize_image(self, name_img, width, height):
        img = Image.open(PATH_IMG_DIR + name_img + '.png')
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        img.save(PATH_IMG_RESIZE_DIR + name_img + 'Resize.png')
        return pygame.image.load(PATH_IMG_RESIZE_DIR + name_img + 'Resize.png').convert()
            
    def menu(self):
        done = False
        pygame.init()
        pygame.mixer.music.load(PATH_MUSIC_MENU)
        pygame.mixer.music.play(loops=-1)

        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)

        while not done:
            try:
                max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'r')
            except:
                max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'w+')
                max_f.write('1')
                max_f.flush()
                max_f.seek(0)
            max_opened_level = int(max_f.readline())
            max_f.close()
            screen.blit(self.back_menu, (0, 0))
            mp = pygame.mouse.get_pos()
            if not self.isChangeLevel:
                if self.isFirstMenu:
                    self.render(screen, font_menu, self.points_in_first_menu, self.menu_point)
                    self.get_menu_point(mp, self.points_in_first_menu)
                elif not self.isFirstMenu and self.isInfo:
                    self.render(screen, font_menu, self.backInChoiceLvl, self.menu_point)
                    self.get_menu_point(mp, self.points_in_second_menu)
                else:
                    self.render(screen, font_menu, self.points_in_second_menu, self.menu_point)
                    self.get_menu_point(mp, self.points_in_second_menu)
            else:
                [screen.blit(self.level[i], (107*constx + 235*constx * (i), 285*consty)) for i in range(max_opened_level)]
                [screen.blit(self.block_level, (107*constx + 235*constx * (self.constPixel - 1), 285*consty)) for self.constPixel in range(max_opened_level + 1, 6)]
                self.render(screen, font_menu, self.backInChoiceLvl, self.menu_point)
                self.get_menu_point(mp, self.points_in_second_menu)
            for e in pygame.event.get():
                if not self.isChangeLevel:
                    if self.isFirstMenu:
                        self.in_first_menu(e, mp)
                    elif not self.isFirstMenu and self.isInfo:
                        self.menu_info(e, mp)
                    else:
                        self.in_second_menu(e, mp)
                else:
                    self.in_choise_lvl_menu(e, mp)
                    
            pygame.display.flip()

class Bonus:
    def __init__(self, game):
        self.game = game  
        self.lvl_text = self.get_resize_image('bonus1', math.ceil(704*constx), math.ceil(101*consty))
        self.lvl_text.set_colorkey((255, 255, 255), RLEACCEL)

        self.image1 = self.get_resize_image('bonus-1', math.ceil(315*constx), math.ceil(367*consty))
        self.image1.set_colorkey((255, 255, 255), RLEACCEL) 
        self.image2 = self.get_resize_image('bonus-2', math.ceil(315*constx), math.ceil(367*consty))
        self.image2.set_colorkey((255, 255, 255), RLEACCEL)  
        self.image3 = self.get_resize_image('bonus-3', math.ceil(315*constx), math.ceil(367*consty))
        self.image3.set_colorkey((255, 255, 255), RLEACCEL)
        self.image4 = self.get_resize_image('bonus-4', math.ceil(315*constx), math.ceil(367*consty))
        self.image4.set_colorkey((255, 255, 255), RLEACCEL)     
        self.image5 = self.get_resize_image('bonus-5', math.ceil(315*constx), math.ceil(367*consty))
        self.image5.set_colorkey((255, 255, 255), RLEACCEL)   
        self.image6 = self.get_resize_image('bonus-6', math.ceil(315*constx), math.ceil(367*consty))
        self.image6.set_colorkey((255, 255, 255), RLEACCEL)   
        self.image7 = self.get_resize_image('bonus-7', math.ceil(315*constx), math.ceil(367*consty))
        self.image7.set_colorkey((255, 255, 255), RLEACCEL)  
        self.down = pygame.image.load(PATH_IMG_RESIZE_LOADING).convert()  


    def __del__(self):
        pass
        # print('Destructor called, Bonus deleted.')

    def get_resize_image(self, name_img, width, height):
        img = Image.open(PATH_IMG_BONUS_DIR + name_img + '.png')
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        img.save(PATH_IMG_RESIZE_DIR + name_img + 'Resize.png')
        return pygame.image.load(PATH_IMG_RESIZE_DIR + name_img + 'Resize.png').convert()

    def run(self, x, e, mp_x, mp_y): 
        self.x = x
        pygame.key.set_repeat(0, 0)
        self.bonus_vec = [0, 0, 0]
        Bonus.bonus_image(self, self.x, self.bonus_vec)
        if self.game.loading  == False:
            screen.blit(self.bonus_vec[0], (120 * constx, 200 * consty))
            screen.blit(self.bonus_vec[1], (520 * constx, 200 * consty))
            screen.blit(self.bonus_vec[2], (920 * constx, 200 * consty))
            screen.blit(self.lvl_text, (370 * constx, 110 * consty))  
        self.bonus = None      
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 :
            if mp_x >= 135 * constx and mp_x < 425 * constx and mp_y > 227 * consty and mp_y < 552 * consty:
                self.bonus = self.x[0] 
                self.game.loading  = True   
                screen.blit(self.down, (0,0))  
                self.game.add_bonus_to_player = True             
                self.save_info(self.bonus)     
            elif mp_x > 527 * constx and mp_x < 822 * constx and mp_y > 227 * consty and mp_y < 552 * consty:
                self.bonus = self.x[1]
                self.game.loading  = True  
                screen.blit(self.down, (0,0)) 
                self.game.add_bonus_to_player = True      
                self.save_info(self.bonus)             
            elif mp_x > 952 * constx and mp_x < 1218 * constx and mp_y > 227 * consty and mp_y < 552 * consty:
                self.bonus = self.x[2]
                self.game.loading = True  
                screen.blit(self.down, (0,0))  
                self.game.add_bonus_to_player = True  
                self.save_info(self.bonus)           

    def bonus_type(self, bonus):
        if bonus == 1:
            self.game.player.health += 1
        if bonus == 2:
            self.game.player.bullets_num += 10
            self.game.player.bullets_num_max += 10        
        if bonus == 3:
            self.game.player.bullet_speed += 2
        if bonus == 4:
            self.game.player.player_speed += 1       
        if bonus == 5:
            self.game.player.reload_speed /= 1.5
        if bonus == 6:
            self.game.poison = True
        if bonus == 7:
            self.game.player.bullet_size += 1                                

    def save_info(self, bonus):
        b = open("save/bonus_after_" + str(index_level) + "_lvl.txt", 'w') 
        b.write(str(bonus))
        b.close()
        if index_level <= 4: 
            l = open(PATH_SAVE_OPEN_LVL, 'w')
            l.write(str(index_level + 1))
            l.close()
        try:
            max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'r')
        except:
            max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'w+')
            max_f.write('1')
            max_f.flush()
            max_f.seek(0)
        max_opened_level = int(max_f.readline())
        max_f.close()
        if max_opened_level < index_level + 1:
            max_f = open(PATH_SAVE_MAX_OPENED_LVL, 'w')
            max_f.write(str(index_level + 1))
            max_f.close()


    def bonus_image(self, x, image_bonus):
        self.x = x
        for i in range(0, 3):
          if self.x[i] == 1:
              self.bonus_vec[i] = self.image1
          if self.x[i] == 2:
              self.bonus_vec[i] = self.image2
          if self.x[i] == 3:
              self.bonus_vec[i] = self.image3
          if self.x[i] == 4:
              self.bonus_vec[i] = self.image4  
          if self.x[i] == 5:
              self.bonus_vec[i] = self.image5     
          if self.x[i] == 6:
             self.bonus_vec[i] = self.image6     
          if self.x[i] == 7:
              self.bonus_vec[i] = self.image7                                            

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super(Mob, self).__init__()
        self.game = game
        if index_level != 5:
            self.surf = pygame.image.load(PATH_IMG_MOB).convert()
        else:
            self.surf = pygame.image.load(PATH_IMG_BOSS).convert()    
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(topleft = (x, y))
        # needs for lee algo
        self.mob_position = (y // self.game.map.cell_size, x // self.game.map.cell_size)
        if index_level !=5:
            pygame.mixer.Channel(2).play(rev_sound, -1)
        else:
            pygame.mixer.Channel(2).play(boss_sound, -1)

        self.path_point = 1
        self.cur_step_len = self.game.map.cell_size
        self.speed = 3 + index_level + self.game.count_boss_speed
        self.field = lee.Field(self.game.map.rows, self.game.map.cols, self.mob_position, \
                                self.game.player.getPosition(), self.game.barriers)
        self.field.emit()
        self.path = self.field.get_path()
        self.path.reverse()

    def __del__(self):
        pass
        # print('Destructor called, Mob deleted.')

    def update(self):

        self.speed = 3 + index_level + self.game.count_boss_speed
        # self.field.show()            
        if self.path_point < len(self.path):
            if self.cur_step_len > 0:
                tx = (self.path[self.path_point][1] - self.mob_position[1]) * self.speed
                ty = (self.path[self.path_point][0] - self.mob_position[0]) * self.speed
                self.rect.move_ip(tx, ty)
                # if pygame.sprite.spritecollideany(self, self.game.bricks): # undo move if collides
                #     self.rect.move_ip(-tx, -ty) 
                # else: # if okay
                    # self.cur_step_len -= self.speed
                self.cur_step_len -= self.speed
            else:
                #self.mob_position = self.path[self.path_point]
                self.path_point += 1
                self.cur_step_len = self.game.map.cell_size

        self.mob_position = (self.rect.y // self.game.map.cell_size, self.rect.x // self.game.map.cell_size)
        if pygame.sprite.spritecollideany(self.game.player, self.game.mobs):
            self.game.player.rect.move_ip(0, self.game.player.damage_of_mobs)
            self.game.player.rect.move_ip(self.game.player.damage_of_mobs, 0)
            self.game.player.texture_collide(self.game.player.damage_of_mobs, self.game.player.damage_of_mobs)
            self.game.player.health -= 1
            pygame.mixer.Channel(1).play(collision_sound)
            if self.game.poison == True:
                if index_level != 5:
                   self.kill() 
            print(self.speed)       

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1, speed,bullet_size, game):
        super(Bullet, self).__init__()
        self.bullet_img = pygame.image.load('assets/images/arrow' + str(bullet_size) + '.png').convert()
        self.bullet_img.set_colorkey((255, 255, 255), RLEACCEL)
        self.game = game
        self.x = x  
        self.y = y
        self.speed = speed
        self.speed_x1 = x1
        self.speed_y1 = y1
        self.rect = self.bullet_img.get_rect(center = (x, y))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                    self.m_x, self.m_y = event.pos
                    l = math.sqrt((self.m_x - self.x)**2 + (self.m_y - self.y)**2)
                    if l > 0:
                        self.speed_x1 = (self.m_x - self.x) / l
                        self.speed_y1 = (self.m_y - self.y) / l

    def __del__(self):
        pass
        # print('Destructor called, Bullet deleted.')

    def update(self):   
        self.x += self.speed * self.speed_x1
        self.y += self.speed * self.speed_y1
        self.rect.move_ip(0, self.speed_y1*self.speed)
        self.rect.move_ip(self.speed_x1*self.speed,0)   
        for entity in self.game.bricks:
            if pygame.sprite.collide_rect(entity, self) and entity.block_type != 'W' and entity.block_type != 'H':
                self.kill()    
                pygame.mixer.Channel(3).play(buulet_to_brick_sound) 
        if index_level != 5:        
            if pygame.sprite.groupcollide(self.game.mobs, self.game.bullets, True, True):
                 pygame.mixer.Channel(1).play(rd.choice(damage_sound))
                 self.kill()              
        else:
            if self.game.boss_hp != self.game.player.bullet_size:
                if pygame.sprite.spritecollideany(self, self.game.mobs):
                    pygame.mixer.Channel(6).play(rd.choice(damage_sound))
                    self.kill()
                    self.game.boss_hp -=  self.game.player.bullet_size     
                    self.game.count_boss += self.game.player.bullet_size  
                    if self.game.count_boss == 60:
                        self.game.count_boss_speed += 7   
                        self.game.animate_boss_hp += 1   
                        self.game.count_boss = 0
            else:
                if pygame.sprite.groupcollide(self.game.mobs, self.game.bullets, True, True):
                 pygame.mixer.Channel(1).play(rd.choice(damage_sound))
                 self.kill()  
                 self.game.animate_boss_hp = 5 
                                                      

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super(Player, self).__init__()
        self.game = game # reference to Game object in which player is playing
        self.orig_img = pygame.image.load(PATH_IMG_PLAYER)
        self.surf = pygame.image.load(PATH_IMG_PLAYER).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # create rect from surface and set initial coords
        self.rect = self.surf.get_rect(topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.dir_x = 0
        self.dir_y = 1
        self.health = 3
        self.player_speed = 5
        self.bullet_speed = 8
        self.bullet_size = 1
        self.bullets_num_max = 15
        self.damage_of_mobs = 50
        self.reload_speed = 1
        self.bullets_num = self.bullets_num_max
        self.state = 'WAIT'

    def __del__(self):
        pass
        # print('Destructor called, Player deleted.')

    def getPosition(self):
        return (self.rect.y // self.game.map.cell_size, \
                self.rect.x // self.game.map.cell_size)
    
    # needs for not stopping in bricks
    def texture_collide(self, x, y):
        if pygame.sprite.spritecollideany(self, self.game.bricks):
            self.rect.move_ip(x, y)
            return self.texture_collide(x, y)        

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -self.player_speed)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(0, self.player_speed)
            if pygame.sprite.spritecollideany(self, self.game.mobs):
                self.rect.move_ip(0, self.damage_of_mobs)
                self.texture_collide(0, self.damage_of_mobs)
                self.health -= 1
                pygame.mixer.Channel(1).play(collision_sound)
            for entity in self.game.terrain_blocks:
                if pygame.sprite.collide_rect(entity, self) and entity.block_type == ':':
                    self.rect.move_ip(0, self.player_speed)

        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.player_speed)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(0, -self.player_speed)
            if pygame.sprite.spritecollideany(self, self.game.mobs):
                self.rect.move_ip(0, -self.damage_of_mobs)
                self.texture_collide(0, -self.damage_of_mobs)
                self.health -= 1
                pygame.mixer.Channel(1).play(collision_sound)
            for entity in self.game.terrain_blocks:
                if pygame.sprite.collide_rect(entity, self) and entity.block_type == ':':
                    self.rect.move_ip(0, -self.player_speed)

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.player_speed, 0)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(self.player_speed, 0)
            if pygame.sprite.spritecollideany(self, self.game.mobs):
                self.rect.move_ip(self.damage_of_mobs, 0)
                self.texture_collide(self.damage_of_mobs, 0)
                self.health -= 1
                pygame.mixer.Channel(1).play(collision_sound)
            for entity in self.game.terrain_blocks:
                if pygame.sprite.collide_rect(entity, self) and entity.block_type == ':':
                    self.rect.move_ip(self.player_speed, 0)

        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.player_speed, 0)
            if pygame.sprite.spritecollideany(self, self.game.bricks):
                self.rect.move_ip(-self.player_speed, 0)
            if pygame.sprite.spritecollideany(self, self.game.mobs):
                self.rect.move_ip(-self.damage_of_mobs, 0)
                self.texture_collide(-self.damage_of_mobs, 0)
                self.health -= 1
                pygame.mixer.Channel(1).play(collision_sound)
            for entity in self.game.terrain_blocks:
                if pygame.sprite.collide_rect(entity, self) and entity.block_type == ':':
                    self.rect.move_ip(-self.player_speed, 0)
        if pygame.sprite.groupcollide(self.game.mobs, self.game.bullets, True, True):
           pygame.mixer.Channel(1).play(rd.choice(damage_sound))
           self.kill()              

        # Keep player on the map
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.map.cols*self.game.map.cell_size:
            self.rect.right = self.game.map.cols*self.game.map.cell_size
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.game.map.rows*self.game.map.cell_size:
            self.rect.bottom = self.game.map.rows*self.game.map.cell_size
    
    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - \
            (self.rect.x - self.game.camera.x + SCREEN_WIDTH//2, self.rect.y - self.game.camera.y + SCREEN_HEIGHT//2)
        angle = direction.angle_to((1, 0))
        self.surf = pygame.transform.rotate(self.orig_img, angle)
        center_x = self.surf.get_width() // 2
        center_y = self.surf.get_height() // 2
        rect_surface = self.rect.copy()  # Create a new rectangle.
        rect_surface.center = (center_x, center_y)  # Move the new rectangle to the center of the new image.
        self.surf = self.surf.subsurface(rect_surface)  # Take out the center of the new image(Cut angles)
        
    def shoot(self):
        if self.state == 'RELOADING':
            return
        if self.bullets_num >= 1:
            self.bullets_num -= 1
            bullet = Bullet(self.rect.x + 15, self.rect.y + 15, self.dir_x, self.dir_y, self.bullet_speed,self.bullet_size , self.game)
            self.game.bullets.add(bullet)
            pygame.mixer.Channel(0).play(shoot_sound)
        else:
            pygame.mixer.Channel(0).play(notshoot_sound)

    def reload(self):

        def reload_bullets(self):
            for _ in range(15):
                if self.bullets_num == self.bullets_num_max:
                    break
                self.bullets_num = min(self.bullets_num_max, self.bullets_num + 5)
                time.sleep(1*self.reload_speed)
            self.state = 'WAIT'

        x = threading.Thread(target=reload_bullets, args=(self,))

        if self.state == 'WAIT':
            self.state = 'RELOADING'
            x.start()

class Pause():
    def __init__(self, game):
        self.game = game

    def __del__(self):
        pass

    def main(self, mp_x, mp_y, e):
        self.option = None 
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if mp_x>=168 * constx and mp_x<453 * constx and mp_y>340 * consty and mp_y<420 * consty:
                self.game.paused = False 
            elif  mp_x>168 * constx and mp_x<453 * constx and mp_y>474 * consty and mp_y<538 * consty:
                self.game.running = False
                game = Game()
                game.main()
            elif mp_x>168 * constx and mp_x<453 * constx and mp_y>595 * consty and mp_y<669 * consty: 
                pygame.mixer.music.load(PATH_MUSIC_MENU)
                pygame.mixer.music.play(loops=-1)
                self.game.running = False                         

class Camera():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.area_width = SCREEN_WIDTH #area_width
        self.area_height = SCREEN_HEIGHT #area_height
        self.speed = 10
        self.inner_bound = 0.7

    def __del__(self):
        pass
        # print('Destructor called, Camera deleted.')

    def follow(self, player, game_map):
        dx, dy = 0, 0
        if (player.rect.x - self.x)*2 > self.area_width*self.inner_bound:
            dx = self.speed
        if (player.rect.x - self.x)*2 < -self.area_width*self.inner_bound:
            dx = -self.speed
        if (player.rect.y - self.y)*2 > self.area_height*self.inner_bound:
            dy = self.speed
        if (player.rect.y - self.y)*2 < -self.area_height*self.inner_bound:
            dy = -self.speed

        new_x, new_y = self.x + dx, self.y + dy

        if new_x - self.area_width // 2 >= 10 and new_x + self.area_width // 2 <= game_map.cols*game_map.cell_size:
            self.x = new_x

        if new_y - self.area_height // 2 >= 0 and new_y + self.area_height // 2 <= game_map.rows*game_map.cell_size:
            self.y = new_y

class Map():
    def __init__(self):
        self.rows = None
        self.cols = None
        self.path = None
        self.matrix = None
        self.cell_size = 72

    def __del__(self):
        pass
        # print('Destructor called, Map deleted.')

    def load_from(self, filepath = 'assets/maps/map3.txt'):
        self.path = filepath
        f = open(filepath)
        self.matrix = f.read().split('\n')
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def cell(self, row, col):
        return self.matrix[row][col]        


class Game():
    def __init__(self):
        global index_level
        surface = pygame.display.get_surface()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = size = surface.get_width(), surface.get_height()
        self.FPS = 60
        self.barriers = []
        self.positionMobs = []
        self.map = Map()
        self.map.load_from('assets/maps/map' + str(index_level) + '.txt')
        self.running = False
        self.add_bonus_to_player = False
        self.isCollision_with_portal = False
        self.loading  = False
        self.paused = False
        self.poison = False
        self.isWaveOfMobs = False
        if index_level == 5:
            self.wave_amount = 0
        else:
            self.wave_amount = 2
        self.boss_hp = 240
        self.count_boss = 0
        self.count_boss_speed = 0
        self.pause_image = self.get_resize_image('in_pause', SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.init()

        self.bonus = Bonus(self)
        self.numbers = list(range(1, 8))
        shuffle(self.numbers)
        self.x=self.numbers[:3]
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
         # Create a set of mobs - Sprite
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.terrain_blocks = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.animate_boss_hp = 1
        self.boss_hp_image = [0, 0, 0, 0, 0, 0]
        for i in range(1, 6):
            self.boss_hp_im = self.get_resize_image('boss_hp-'+ str(i), 450, 130)
            self.boss_hp_image[i] = pygame.image.load('assets/images/Resize/boss_hp-' + str(i) + 'Resize.png').convert()
            self.boss_hp_image[i].set_colorkey((255, 255, 255), RLEACCEL)
        

    def __del__(self):
        pass
        # print('Destructor called, Game deleted.')

    def get_resize_image(self, name_img, width, height):
        img = Image.open(PATH_IMG_DIR + name_img + '.png')
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        img.save(PATH_IMG_RESIZE_DIR + name_img + 'Resize.png')
        return pygame.image.load(PATH_IMG_RESIZE_DIR + name_img + 'Resize.png').convert()

    def delete_all_objects(self):
        del self.bonus
        del self.map
        self.mobs.empty()
        self.bullets.empty()
        self.bricks.empty()
        self.terrain_blocks.empty()
        for mob in self.mobs:
            del mob
        for bullet in self.bullets:
            del bullet
        for brick in self.bricks:
            del brick
        for terrblock in self.terrain_blocks:
            del terrblock
        del self.player
        del self.camera

    def mobs_path_to_player(self):
        for mob in self.mobs:
            #print('calculating path...')
            mob.field = lee.Field(self.map.rows, self.map.cols, mob.mob_position, \
                                self.player.getPosition(), self.barriers)
            mob.field.emit()
            mob.path = mob.field.get_path()
            mob.path.reverse()
            #print(mob.path, 'mob pos = ', mob.mob_position, 'player pos = ', self.getPosition())
            mob.path_point = 1
            mob.cur_step_len = self.map.cell_size
            #mob.field.show()
        #print(self.getPosition(), self.game.player.getPosition())

    def draw_map(self):
        if not self.isWaveOfMobs:
            for i in range(self.map.rows):
                for j in range(self.map.cols):
                    cell = self.map.cell(i, j)
                    if cell == '#':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '$':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '*':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '&':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '<':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '>':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '{':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '}':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '?':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == ';':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '^':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '-':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))
                    elif cell == '.':
                        new_terrain_block = TerrainBlock(j*self.map.cell_size, i*self.map.cell_size, 1, index_level)
                        self.terrain_blocks.add(new_terrain_block)
                    elif cell == "'":
                        new_terrain_block = TerrainBlock(j*self.map.cell_size, i*self.map.cell_size, 1, index_level)
                        self.terrain_blocks.add(new_terrain_block)
                    elif cell == ',':
                        new_terrain_block = TerrainBlock(j*self.map.cell_size, i*self.map.cell_size, 1, index_level)
                        self.terrain_blocks.add(new_terrain_block)
                    elif cell == ":":
                        new_terrain_block = TerrainBlock(j*self.map.cell_size, i*self.map.cell_size, cell, index_level)
                        self.terrain_blocks.add(new_terrain_block)  
                    elif cell == 'B':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))  
                    elif cell == 'q':
                        new_brick = Brick(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(new_brick)
                        self.barriers.append((i, j))             
                    elif cell == '1':
                        house1 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(house1)
                        self.barriers.append((i, j))
                    elif cell == '2':
                        house2 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(house2)    
                        self.barriers.append((i, j))
                    elif cell == '3':
                        house3 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(house3)  
                        self.barriers.append((i, j))       
                    elif cell == '4':
                        house4 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(house4)     
                        self.barriers.append((i, j))           
                    elif cell == '5':
                        house5 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(house5)  
                        self.barriers.append((i, j))
                    elif cell == '6':
                        house6 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(house6)  
                        self.barriers.append((i, j))
                    elif cell == '7':
                        most1 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.terrain_blocks.add(most1)  
                    elif cell == '8':
                        most2 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.terrain_blocks.add(most2)     
                    elif cell == '9':
                        most3 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.terrain_blocks.add(most3)  
                    elif cell == '0':
                        most4 = House(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.terrain_blocks.add(most4) 
                    elif cell == 'T':
                        tree1 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree1) 
                        self.barriers.append((i, j))
                    elif cell == 'O':
                        tree2 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree2) 
                        self.barriers.append((i, j))
                    elif cell == 'A':
                        tree3 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree3) 
                        self.barriers.append((i, j))
                    elif cell == 'X':
                        tree4 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree4) 
                        self.barriers.append((i, j))  
                    elif cell == 't':
                        tree11 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree11) 
                        self.barriers.append((i, j))
                    elif cell == 'o':
                        tree12 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree12) 
                        self.barriers.append((i, j))
                    elif cell == 'a':
                        tree13 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree13) 
                        self.barriers.append((i, j))
                    elif cell == 'x':
                        tree14 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree14) 
                        self.barriers.append((i, j))       
                    elif cell == 'l':
                        tree21 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree21) 
                        self.barriers.append((i, j))  
                    elif cell == 'k':
                        tree22 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree22) 
                        self.barriers.append((i, j))                 
                    elif cell == 'j':
                        tree23 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree23) 
                        self.barriers.append((i, j))                 
                    elif cell == 'u':
                        tree24 = Tree(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(tree24) 
                        self.barriers.append((i, j))                                                                                            
                    elif cell == 'W':
                        water1 = Water(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(water1)
                        self.barriers.append((i, j))     
                    elif cell == 'H':
                        water2 = Water(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.bricks.add(water2)  
                        self.barriers.append((i, j))          
                    elif cell == 'D' or cell == 'd':
                        door = Door(j*self.map.cell_size, i*self.map.cell_size, cell + " ", index_level)
                        self.bricks.add(door)
                        self.barriers.append((i, j))
                        open_door = Door(j*self.map.cell_size, i*self.map.cell_size, cell, index_level)
                        self.terrain_blocks.add(open_door)
                    elif cell == 'P':
                        portal = Portal(j*self.map.cell_size, i*self.map.cell_size, cell)
                        self.terrain_blocks.add(portal)
                    elif cell == '!': # Create a player - Sprite
                        self.player = Player(self, self.all_sprites)
                        new_terrain_block = TerrainBlock(j*self.map.cell_size, i*self.map.cell_size, 1, index_level)
                        self.all_sprites.add(self.player)
                        self.terrain_blocks.add(new_terrain_block)
                    elif cell == '@':
                        self.positionMobs.append((i, j))
                        new_terrain_block = TerrainBlock(j*self.map.cell_size, i*self.map.cell_size, 1, index_level)
                        self.terrain_blocks.add(new_terrain_block)                            
                    else:
                        print('map error: incorrect cell type', cell)                  
        for mobPos in self.positionMobs:
            new_mob = Mob(mobPos[1]*self.map.cell_size, mobPos[0]*self.map.cell_size, self)
            self.mobs.add(new_mob)

    def init_cam(self):
        cam_x, cam_y = self.player.rect.x, self.player.rect.y
        self.camera = Camera(cam_x, cam_y)

    def main(self):
        global index_level
        pygame.mixer.music.load('assets/music/'+ str(index_level)+'_level.mp3')
        pygame.mixer.music.play(loops=-1)
        self.running = True # flag that show is game running or not
        pygame.event.set_grab(True)
        # create own event - reload to build next path in alg Lee for mobs
        update_paths = pygame.USEREVENT + 1
        pygame.time.set_timer(update_paths, 3000)
        
        update_wave_of_mobs = pygame.USEREVENT + 2
        pygame.time.set_timer(update_wave_of_mobs, 15000)
        self.draw_map()
        
        for i in range(1, index_level):
            r = open("save/bonus_after_" + str(i) + "_lvl.txt", 'r')
            read_bonus = r.readline()
            read_bonus = int(read_bonus)
            self.bonus.bonus_type(read_bonus)     

        self.init_cam()
        while self.player.health > 0 and self.running and index_level <= 5:   # this cicle defines health of our player
            self.clock.tick(self.FPS)                    # delay according to fps

            for event in pygame.event.get():             # check events
                if event.type == pygame.KEYDOWN:         # when user hits some button
                    if event.key == pygame.K_ESCAPE:     # Esc -> quit
                        self.paused = not self.paused
                        screen.blit(self.pause_image, (0 * constx, 0 * consty))
                    elif event.key == pygame.K_m:     
                        pygame.mixer.music.pause() 
                    elif event.key == pygame.K_n:     
                        pygame.mixer.music.unpause()     
                    elif event.key == pygame.K_r:
                        if self.player.bullets_num <= 5:
                            pygame.mixer.Channel(0).play(reload_sound)
                            self.player.reload()
       
                elif event.type == pygame.MOUSEBUTTONDOWN:         
                    if event.button == 1:
                        if not self.paused:
                           self.player.shoot()
                elif event.type == pygame.MOUSEMOTION:
                    m_x, m_y = event.pos
                    l = math.sqrt((m_x - (self.player.rect.x - self.camera.x + SCREEN_WIDTH//2))**2 + (m_y - (self.player.rect.y - self.camera.y + SCREEN_HEIGHT//2))**2)
                    if l > 0:
                        self.player.dir_x = (m_x - (self.player.rect.x - self.camera.x + SCREEN_WIDTH//2)) / l
                        self.player.dir_y = (m_y - (self.player.rect.y - self.camera.y + SCREEN_HEIGHT//2)) / l
                elif event.type == pygame.QUIT:   # if user closes the widow -> quit
                    self.running = False
                elif event.type == update_paths:
                    self.mobs_path_to_player()
                elif event.type == update_wave_of_mobs and self.wave_amount > 0 and index_level != 5:
                    self.isWaveOfMobs = True
                    self.draw_map() # without classic objects, only spawn of mobs
                    self.wave_amount -= 1

            # Get all the keys currently pressed
            pressed_keys = pygame.key.get_pressed()
            # Rotating sprite depending on mouse motion
            if not self.paused:
                self.player.point_at(*pygame.mouse.get_pos())
                # Update the player sprite based on user keypresses
                self.player.update(pressed_keys)
                # Update mobs movement
                self.mobs.update()
                self.bullets.update()
                #self.screen.fill((0, 0, 0))

                # all object are rendered according to camera position and center of the screen
                
                if not self.isCollision_with_portal:
                    for entity in self.terrain_blocks:
                        if pygame.sprite.collide_rect(entity, self.player) and entity.block_type == 'P':
                            self.isCollision_with_portal = True
                            self.player.state = "RELOADING"
                            if not self.add_bonus_to_player:
                                if index_level == 5:
                                    pygame.mixer.music.pause()
                                    pygame.mixer.music.load(PATH_MUSIC_MENU)
                                    pygame.mixer.music.play(loops=-1)
                                    self.running = False
                                else:
                                    self.bonus.run(self.x, event, *pygame.mouse.get_pos())   
                            else:
                                self.running = False
                                pass
                            break
                        else:
                            if self.loading  == False:
                                self.screen.blit(entity.surf, (entity.rect.x - self.camera.x + SCREEN_WIDTH//2, entity.rect.y - self.camera.y + SCREEN_HEIGHT//2))
                                self.isCollision_with_portal = False
                    for entity in self.bricks:
                        if not self.isCollision_with_portal:
                            self.screen.blit(entity.surf, (entity.rect.x - self.camera.x + SCREEN_WIDTH//2, entity.rect.y - self.camera.y + SCREEN_HEIGHT//2))
                    # Draw mobs on the screen
                    for entity in self.mobs:
                        self.screen.blit(entity.surf, (entity.rect.x - self.camera.x + SCREEN_WIDTH//2, entity.rect.y - self.camera.y + SCREEN_HEIGHT//2))
                self.isCollision_with_portal = False
                # Draw the player on the screen
                if self.loading  == False:  
                     self.screen.blit(self.player.surf, (self.player.rect.x - self.camera.x + SCREEN_WIDTH//2, self.player.rect.y - self.camera.y + SCREEN_HEIGHT//2))
                # Camera follows the player
                self.camera.follow(self.player, self.map)
                
                if len(self.mobs.sprites()) == 0 and self.wave_amount == 0:
                    pygame.mixer.Channel(2).pause()
                    for entity in self.bricks:
                        if entity.block_type == 'D ' or entity.block_type == 'd ':
                            pygame.mixer.Channel(4).play(portal_sound)
                            self.bricks.remove(entity)
                for entity in self.bullets:
                    if entity.x <= self.map.cols*self.map.cell_size:
                        screen.blit(entity.bullet_img, (entity.rect.x - self.camera.x + SCREEN_WIDTH//2, entity.rect.y - self.camera.y + SCREEN_HEIGHT//2))
            else:
                pause = Pause(self)
                pause.main(*pygame.mouse.get_pos(),event)
            # Draw fps counter
            fps = self.font.render('FPS: ' + str(int(self.clock.get_fps())), True, pygame.Color('white'))
            hl = self.font.render(str(self.player.health),True, pygame.Color('white'))
            bl = self.font.render(':'+ str(self.player.bullets_num)+'/'+str(self.player.bullets_num_max) , True, pygame.Color('white'))
            health_image = pygame.image.load(PATH_IMG_HEALTH).convert()
            health_image.set_colorkey((0, 0, 0), RLEACCEL)   
            bullet_image = pygame.image.load(PATH_IMG_BULLET).convert()
            bullet_image.set_colorkey((0, 0, 0), RLEACCEL)  
            if not self.paused: 
                if self.loading  == False:              
                    self.screen.blit(health_image,(math.ceil(1150*constx),math.ceil(20)))
                    self.screen.blit(bullet_image,(math.ceil(1240*constx),math.ceil(20)))
                    self.screen.blit(fps, (math.ceil(40*constx),  40))
                    self.screen.blit(hl, (math.ceil(1173*constx*consth), 40))
                    self.screen.blit(bl, (math.ceil(1290*constx), 40))
                    if index_level == 5:
                        i = self.animate_boss_hp
                        self.screen.blit(self.boss_hp_image[i],(math.ceil(10),math.ceil(640 *consty)))
            # Update the display
            pygame.display.flip()

        # check status of player's health 
        if self.player.health <= 0:
            pygame.mixer.music.pause()
            pygame.mixer.music.load(PATH_MUSIC_MENU)
            pygame.mixer.music.play(loops=-1)
            self.running = False
        self.delete_all_objects()

pygame.font.init()     

if __name__ == "__main__":
    menu = Menu()
    menu.menu()