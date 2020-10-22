from display import *
import random

class Ship(Display):

    """A class to create the player/enemy ship."""
    # default constructor
    def __init__(self, hp, x, y, speed):
        Display.__init__(self)
        self.health = hp
        self.x = x
        self.y = y
        self.move_speed = speed
        self.ship_img = None
        self.laser_img = None

        self.dx, self.dy = self.move_speed, self.move_speed

        #self.display = display
        self.ship = None

    def movement(self):
        if self.x >= self.width - 64 or self.x <= 0:
            self.dx = -self.dx
        self.x += self.dx
        if self.y >= self.height - 500 - 64 or self.y <= 50:
            self.dy = -self.dy
        self.y += self.dy

    def collision(self, obj2):
        return self.ship.colliderect(obj2)



    '''
    # Loading the image of the ship
    self.image = pygame.image.load('') #blank file location for now
    self.rect = self.image.get_rect() #game elements treated as rectangles
    '''
