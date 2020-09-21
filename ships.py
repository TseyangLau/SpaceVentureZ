import pygame
from shipBase import Ship


class Player(Ship):
    def __init__(self, hp, x, y, speed):
        super(Player, self).__init__(hp, x, y, speed)
        self.playerModel = pygame.image.load('player.png')

    def draw(self, window):
        window.blit(self.playerModel, (self.x, self.y))


class Enemy(Ship):
    def __init__(self, hp, x, y, speed):
        super(Enemy, self).__init__(hp, x, y, speed)
        self.enemyModel = pygame.image.load('enemy.png')

    def draw(self, window):
        window.blit(self.enemyModel, (self.x, self.y))
