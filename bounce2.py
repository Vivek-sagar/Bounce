import pygame, sys
from pygame.sprite import Sprite
from pygame.locals import *

class ball(Sprite):

    image = None
    
    def __init__(
        self, screen, img_filename, init_position, init_direction,  speed):
        """Initialises the ball"""
        Sprite.__init__(self)
        self.screen = screen
        self.x = 0
        self.y = init_position
        self.speed = speed
        self.direction = init_direction
        
        #Efficient way to load many instances of the same class.
        #Loads the png image only once!
        if ball.image is None:
            ball.image =  pygame.image.load(img_filename).convert()
        self.image = ball.image

        self.rect = self.image.get_rect()
        self.pull = 0.3
        self.bounce = 10

    def update(self):
        """ Updates the ball position"""

        self.image_w, self.image_h = self.image.get_size()
        bounds_rect = self.screen.get_rect().inflate(-self.image_w,
                                                     -self.image_h)

        self.x += self.speed*self.direction
        if (self.x < bounds_rect.left):
            self.x = bounds_rect.left
            self.direction = 1
        elif (self.x > bounds_rect.right):
            self.x = bounds_rect.right
            self.direction = -1

        self.y -= self.bounce
        self.bounce -= self.pull

        if (self.y > bounds_rect.bottom):
            self.y = bounds_rect.bottom
            self.bounce = 10

    def get_pos(self):
        return (self.x, self.y)

    def blitme(self):

        self.screen.blit(self.image, (self.x-self.image_w/2,
                                      self.y-self.image_h/2))

class player(Sprite):

    def __init__(self, screen, img_filename, init_position, speed):
        """Initialises the player class"""
        Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(img_filename).convert_alpha()
        self.x = 0
        self.y = init_position
        self.direction = 1
        self.speed = speed
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect()

    def update(self, direction):
        """Moves the player left or right based on the argument"""
        
        self.image_w, self.image_h = self.image.get_size()
        bounds_rect = self.screen.get_rect().inflate(-self.image_w, -self.image_h)

        if direction > 0:
            self.x += self.speed
            if self.x > bounds_rect.right :
                self.x -= self.speed
        elif direction < 0:
            self.x -= self.speed
            if self.x < bounds_rect.left :
                self.x += self.speed

    def get_pos(self):
        return (self.x, self.y)
        
    def blitme(self):
        self.screen.blit(self.image, (self.x-self.image_w/2,
                                      self.y-self.image_h/2))
        
        


def run_game():
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
    BG_COLOR = 200, 200, 100
    img_filename = "images/ball.png"
    player_img_filename = "images/nosey_bar.png"

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    bl = []
    bl.append(ball(screen, img_filename, 0, 1, 1))
    bl.append(ball(screen, img_filename, 0, 1, 3))

    pl = player(screen, player_img_filename, SCREEN_HEIGHT-20, 10)

    player_dir = 0
    
    while True:

        time_passed = clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == KEYDOWN):
                if (event.key == K_d):
                    player_dir = 1
                elif (event.key == K_a):
                    player_dir = -1
            elif (event.type == KEYUP):
                if (event.key == K_d):
                    player_dir = 0
                elif (event.key == K_a):
                    player_dir = 0
            elif (  event.type == pygame.MOUSEBUTTONDOWN and
                    pygame.mouse.get_pressed()[0]):
                bl.append(ball(screen, img_filename, 0, 1, 2))

        screen.fill(BG_COLOR)

        #Update all objects
        for bal in bl:
            bal.update()
        pl.update(player_dir)

        #Collision detection
        (player_x, player_y) = pl.get_pos()
        player_w, player_h = bal.image.get_size()
        for bal in bl:
            (ball_x, ball_y) = bal.get_pos()
            ball_w, ball_h = bal.image.get_size()
            print pl.rect.colliderect(bal.rect)
            if ball_y+ball_h > player_y:
                if player_x < ball_x+ball_w \
                and player_x+player_w > ball_x:
                    pass
            
        
        #Blit all objects to screen
        pl.blitme()
        for bal in bl:
            bal.blitme()
        

        pygame.display.flip()

run_game()
     
