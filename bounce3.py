import pygame, sys, os
from pygame.sprite import Sprite
from random import randint, choice
from pygame.locals import *

class ball(Sprite):

    image = None
    
    def __init__(
        self, screen, img_filename, init_position, init_direction,  speed):
        """Initialises the ball"""
        Sprite.__init__(self)
        self.screen = screen
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
        bounds_rect = self.screen.get_rect()
        self.rect = self.rect.move(self.speed*self.direction, 0)
        if (self.rect.left < bounds_rect.left):
            self.direction = 1
            self.rect = self.rect.move(2*self.speed*self.direction, 0)          
        elif (self.rect.right > bounds_rect.right):
            self.direction = -1
            self.rect = self.rect.move(2*self.speed*self.direction, 0)

        self.rect = self.rect.move(0,-self.bounce)
        self.bounce -= self.pull

        if (self.rect.bottom > bounds_rect.bottom):
            self.bounce = 10
            self.rect = self.rect.move(0,-self.bounce)

    def blitme(self):
        self.screen.blit(self.image, self.rect.topleft)
        

class player(Sprite):

    def __init__(self, screen, img_filename, init_position, speed):
        """Initialises the player class"""
        Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(img_filename).convert_alpha()
        self.direction = 1
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = (0, init_position)

    def update(self, direction):
        """Moves the player left or right based on the argument"""
        bounds_rect = self.screen.get_rect()
        if direction > 0:
            self.rect = self.rect.move(self.speed, 0)
            if self.rect.right > bounds_rect.right :
                self.rect.right = bounds_rect.right
        elif direction < 0:
            self.rect = self.rect.move(-self.speed, 0)
            if self.rect.left < bounds_rect.left :
                self.rect.left = bounds_rect.left
        
    def blitme(self):
        self.screen.blit(self.image,self.rect.topleft)

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        print "wazzaa"
        return NoneSound()
    
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound
        
def draw_rimmed_box(screen, box_rect, box_color, 
                    rim_width=0, 
                    rim_color=Color('black')):
    """ Draw a rimmed box on the given surface. The rim is drawn
        outside the box rect.
    """
    if rim_width:
        rim_rect = Rect(box_rect.left - rim_width,
                        box_rect.top - rim_width,
                        box_rect.width + rim_width * 2,
                        box_rect.height + rim_width * 2)
        pygame.draw.rect(screen, rim_color, rim_rect)
    
    pygame.draw.rect(screen, box_color, box_rect)
    
def score_ticker(screen, score, lives, rect):
    draw_rimmed_box(screen, rect, Color(150,150,75,1), 4, Color('black'))
    my_font = pygame.font.SysFont('copperplate gothic', 18)
    message1 = my_font.render(score, True, Color('black'))
    message2 = my_font.render(lives, True, Color('black'))
    screen.blit(message1, rect)
    screen.blit(message2, rect.move(0, message1.get_height()))


def end_game(screen, counter):
    i = 0
    r = 200
    g = 100
    b = 100
    my_font = pygame.font.SysFont('arial', 200)
    rect = Rect(200,100, 100, 100)
    message = my_font.render(str(counter), True, Color('grey'))
    while i<100:
        i+=1
        r -= 2
        g -= 1
        b -= 1
        bg_color = (r,g,b)       
        screen.fill(bg_color)
        screen.blit(message, rect)
        pygame.display.flip()
        pygame.time.wait(30)
        
    sys.exit()
    
def run_game():
    SCREEN_WIDTH, SCREEN_HEIGHT = 800,400
    DEFAULT_BG_COLOR = 200, 200, 100
    HIT_BG_COLOR = 200,100,100
    SCORE_RECT = Rect(500,50,120,50)
    img_filename = "images/ball.png"
    player_img_filename = "images/nosey_bar.png"

    pygame.init()
    pygame.mixer.init()
    
    hit_sound = load_sound('bottlepop.wav')

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    pygame.mixer.music.load("data/urbanspy.mp3")
    pygame.mixer.music.play(-1)
    
    bl = []
    bl.append(ball(screen, img_filename, 0, 1, randint(1,5)))
    bl.append(ball(screen, img_filename, 0, 1, randint(1,5)))

    pl = player(screen, player_img_filename, SCREEN_HEIGHT, 10)

    player_dir = 0

    lives = 2
    hit_flag = 0

    counter = 0

    end_flag = 0

    running = True
    
    while running:

        counter += 1

     
        if (counter%500 == 0):
            bl.append(ball(screen, img_filename, 0, 1, randint(1,5)))
            #counter = 0
        
        pygame.time.wait(10)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == KEYDOWN):
                if (event.key == K_RIGHT):
                    player_dir = 1
                elif (event.key == K_LEFT):
                    player_dir = -1
            elif (event.type == KEYUP):
                if (event.key == K_RIGHT):
                    player_dir = 0
                elif (event.key == K_LEFT):
                    player_dir = 0
            elif (  event.type == pygame.MOUSEBUTTONDOWN and
                    pygame.mouse.get_pressed()[0]):
                bl.append(ball(screen, img_filename, 0, 1, randint(1,5)))

        #Update all objects
                  
        for bal in bl:
            bal.update()
        pl.update(player_dir)
        
        pla = pl.rect.inflate(-5, -5)
        #Collision detection
    
        for bal in bl:
            ball_rect = bal.rect.inflate(-10,-10)
            if (pla.colliderect(ball_rect) == 1):
                bg_color = HIT_BG_COLOR
                hit_sound.play()
                hit_flag = 1
                break
            else:
                bg_color = DEFAULT_BG_COLOR
                    
        if hit_flag == 1 and bg_color == DEFAULT_BG_COLOR:
            lives -= 1
            hit_flag = 0
            if lives < 0:
                end_game(screen, counter/10)
        

        screen.fill(bg_color)
        
        #Blit all objects to screen
        pl.blitme()
        for bal in bl:
            bal.blitme()
        msg1 = 'Score : ' + str(counter/10)
        msg2 = 'Lives : ' + str(lives)
        score_ticker(screen, msg1, msg2, SCORE_RECT)
   
        pygame.display.flip()

run_game()
