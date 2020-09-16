import pygame

class Ship:
    """A class to create the player ship."""

    # default constructor
    def __init__(self, hp, x, y, speed):
        self.health = hp
        self.x = x
        self.y = y
        self.move_speed = speed

    # draw a temporary ship
    # add draw() comments later on how it works
    def draw(self, window):
        pygame.Color.r
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))

    '''
    # Loading the image of the ship
    self.image = pygame.image.load('') #blank file location for now
    self.rect = self.image.get_rect() #game elements treated as rectangles
    '''
