from display import *
import random
from math import *
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
        self.ship = None

    def movement(self):
        if self.x >= self.width - 64 or self.x <= 0:
            self.dx = -self.dx
        self.x += self.dx
        if self.y >= self.height - 100 or self.y <= 0:
            self.dy = -self.dy
        self.y += self.dy

    def collision(self, obj2):
        return self.ship.colliderect(obj2)

    '''Added the following by isabel for unique auto movement and tracking of player'''
    def distance(self, obj):
        return sqrt((self.x - obj.x)**2 + (self.y - obj.y) ** 2)

    def auto_movement(self, obj):
        dis = self.distance(obj)
        if dis < 150:
            if (self.x - obj.x) < (self.y - obj.y):
                if self.x <= obj.x:
                    self.x += self.move_speed
                else:
                    self.y -= self.move_speed
            else:
                if self.y <= obj.y:
                    self.y += self.move_speed
                elif self.y > obj.y:
                    self.x -= self.move_speed
        else:
            self.movement()





    '''
    # Loading the image of the ship
    self.image = pygame.image.load('') #blank file location for now
    self.rect = self.image.get_rect() #game elements treated as rectangles
    '''
