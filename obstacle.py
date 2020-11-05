from display import *
import random 

'''Obstacle cvbe Class for obstacles in the game 
   Inherits display to keep the obstacles within the boundaries 
   of the game display handles obstacles movement as well as collisions'''
class Obstacle(Display):
    def __init__(self, x, y, w=25, h=25):
        Display.__init__(self)
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.window = self.display
        self.ob_rect = None
        self.speed = random.randint(2, 3)
        self.dx, self.dy = self.speed, self.speed

    '''checks collision of element with object'''
    def coll(self, element):
        return self.ob_rect.colliderect(element)

    ''' moves the object on display bounces off walls'''
    def move(self):
        if self.x >= self.width - self.w or self.x <= 0:
            self.dx = -self.dx
        self.x += self.dx
        if self.y >= self.height-500 - self.h or self.y <= 50:
            self.dy = -self.dy
        self.y += self.dy
        
class BlackHole:
    def __init__(self, x, y, radius, display):
        Obstacle.__init__(self, x, y)
        '''size of black-hole'''
        self.w = 80
        self.h = 80
        '''image handling'''
        self.bh_image = pygame.image.load('game_images/black-hole.png')
        self.bh_pulse = pygame.image.load('game_images/black-hole-pulse.png')


    ''' draws the black-hole on the display'''

    def draw(self):
        self.ob_rect = self.bh_image.get_rect()
        self.bh = pygame.draw.circle(self.window, (0, 255, 0), (self.x, self.y), self.radius)
        #self.window.blit(pygame.transform.scale(self.black_hole_img, (self.w, self.h)), (self.x, self.y))

    ''' black-hole pulses when an objects is captured'''

    def pulse(self):
        bh_pulse_rect = self.bh_pulse.get_rect()
        bh_pulse_rect.x, bh_pulse_rect.y, bh_pulse_rect.w, bh_pulse_rect.h = self.x, self.y, self.w + 10, self.h + 10
        self.window.blit(self.bh_pulse, bh_pulse_rect)
        '''pulse sfx'''
        # royalty free sfx from zapsplat.com
        black_hole_sound = pygame.mixer.Sound('game_audio/black_hole.wav')  # load sfx
        black_hole_sound.play()  # play sfx

    '''returns true if the element entered within the surface area of the blackhole'''

    def entered_bh(self, element):
        return self.coll(element)

    
class Asteroids(Obstacle):
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y)
        # health of asteroid
        self.hp = 5
        '''image and rect handling'''
        self.as_image = pygame.image.load("game_images/asteroid.png")
    '''draws the asteroids on display'''
    def draw(self):
        self.ob_rect = self.as_image.get_rect()
        self.ob_rect.x, self.ob_rect.y, self.ob_rect.w, self.ob_rect.h = self.x, self.y, self.w, self.h
        self.window.blit(self.as_image, self.ob_rect)

    '''explosion? debating whether to keep this image to be used when removing include sound here'''
    def explode(self):
        pass
