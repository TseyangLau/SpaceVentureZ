import pygame
from shipBase import Ship


class Player(Ship):
    def __init__(self, hp, x, y, speed):
        super(Player, self).__init__(hp, x, y, speed)

    def draw(self, window):
        pygame.Color.r
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))


class Enemy(Ship):
    def __init__(self, hp, x, y, speed):
        super(Enemy, self).__init__(hp, x, y, speed)

    def draw(self, window):
        pygame.Color.b
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 40, 40))
