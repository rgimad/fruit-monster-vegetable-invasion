import sys
import math
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
#SCREEN_WIDTH = 1600
#SCREEN_HEIGHT = 900
FPS = 60

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((255, 255, 255))
        # create rect from surface and set initial coords (by default they;re (0, 0
        self.rect = self.surf.get_rect(topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.dir_x = 0
        self.dir_y = 1

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT



def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    player = Player() # create a player
    
    running = True # flag that show is game running or not

    while running:
        clock.tick(FPS)  # delay according to fps
        
        for event in pygame.event.get(): # check events
            
            if event.type == KEYDOWN:         # when user hits some button
                if event.key == K_ESCAPE:     # Esc -> quit
                    running = False

            elif event.type == pygame.MOUSEMOTION:
                m_x, m_y = event.pos
                l = math.sqrt((m_x - player.rect.x)**2 + (m_y - player.rect.y)**2)
                if l > 0:
                    player.dir_x = (m_x - player.rect.x) / l
                    player.dir_y = (m_y - player.rect.y) / l
                
                    
            elif event.type == pygame.QUIT:   # if user closes the widow -> quit
                running = False

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        screen.fill((0, 0, 0))

        # Draw the player on the screen
        screen.blit(player.surf, player.rect)

        pygame.draw.line(screen, (255, 0, 0), 
                 [player.rect.x, player.rect.y], 
                 [player.rect.x + 700*player.dir_x, player.rect.y + 700*player.dir_y], 3)

        # update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
