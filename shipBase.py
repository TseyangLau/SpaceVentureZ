import pygame

class Ship:

    """A class to create the player/enemy ship."""

    # default constructor
    def __init__(self, hp, x, y, speed):
        self.health = hp
        self.x = x
        self.y = y
        self.move_speed = speed
        self.ship_img = None
        self.laser_img = None

    def movement(self, keys, boundary):
        if keys[pygame.K_LEFT] and self.x > self.move_speed - 10:
            self.x -= self.move_speed
        if keys[pygame.K_RIGHT] and self.x < boundary[0] - 50:
            self.x += self.move_speed
        if keys[pygame.K_UP] and self.y > self.move_speed - 10:
            self.y -= self.move_speed
        if keys[pygame.K_DOWN] and self.y < boundary[1] - 40 - self.move_speed:
            self.y += self.move_speed



    '''
    # Loading the image of the ship
    self.image = pygame.image.load('') #blank file location for now
    self.rect = self.image.get_rect() #game elements treated as rectangles
    '''
