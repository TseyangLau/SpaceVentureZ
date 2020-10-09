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

        #self.display = display
        self.ship = None

    def movement(self, keys, boundary):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > self.move_speed - 20:
            self.x -= self.move_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < boundary[0] - 50:
            self.x += self.move_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > self.move_speed - 10:
            self.y -= self.move_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < boundary[1] - 50 - self.move_speed:
            self.y += self.move_speed

    def collision(self, obj2):
        if self.ship.colliderect(obj2):
            #print('Touched')
            return True
        else:
            return False

    '''
    # Loading the image of the ship
    self.image = pygame.image.load('') #blank file location for now
    self.rect = self.image.get_rect() #game elements treated as rectangles
    '''
