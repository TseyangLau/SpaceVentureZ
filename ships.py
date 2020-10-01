import pygame
from shipBase import Ship
from laser import Laser


class Player(Ship):
    def __init__(self, hp, x, y, speed, display):
        super(Player, self).__init__(hp, x, y, speed)
        self.display = display
        self.playerModel = pygame.image.load('game_images/Player.png')

        # testing purposes
        self.x, self.y = x, y
        self.laser = Laser(x, y, self.display)
        # storing lasers into a group
        self.lasers = pygame.sprite.Group()

    def draw(self, window):
        # self.ship = pygame.draw.rect(window, (0, 0, 255), (self.x, self.y, 64, 64))
        self.ship = self.playerModel.get_rect() # gets the rect of image
        self.ship.x, self.ship.y, self.ship.w, self.ship.h = self.x, self.y, 64, 64
        window.blit(self.playerModel, (self.x, self.y))

    def fire_laser(self, keys):
        if keys[pygame.K_SPACE]:
            new_laser = Laser(self.x, self.y ,self.display)
            self.lasers.add(new_laser)
            # new_laser.update() #moving (should be updating)
        for laser in self.lasers.sprites():
            laser.draw_laser()
            laser.update()

class Enemy(Ship):
    def __init__(self, hp, x, y, speed):
        super(Enemy, self).__init__(hp, x, y, speed)
        self.enemyModel = pygame.image.load('game_images/Enemy.png')

    def draw(self, window):
        # self.ship = pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 40, 40))
        self.ship = self.enemyModel.get_rect()  # gets the rect of image
        self.ship.x, self.ship.y, self.ship.w, self.ship.h = self.x, self.y, 64, 64
        window.blit(self.enemyModel, (self.x, self.y))
