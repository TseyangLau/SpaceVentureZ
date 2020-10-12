import pygame
import random
from shipBase import Ship
from laser import Laser
import math


class Player(Ship):
    def __init__(self, hp, x, y, speed, display):
        super(Player, self).__init__(hp, x, y, speed)
        self.display = display
        self.playerModel = pygame.image.load('game_images/Player.png')

        # testing purposes
        self.x, self.y = x, y
        # storing lasers into a group
        self.lasers = pygame.sprite.Group()
        print("This iss in the init of SHIP " , len(self.lasers.sprites()))

    def draw(self, window):
        self.ship = self.playerModel.get_rect() # gets the rect of image
        self.ship.x, self.ship.y, self.ship.w, self.ship.h = self.x, self.y, 64, 64
        window.blit(self.playerModel, (self.x, self.y))

    def fire_laser(self, keys):
        if keys[pygame.K_SPACE]:
            new_laser = Laser(self.x, self.y, self.display)
            if len(self.lasers.sprites()) > 11:
                # I don't know yet
                pass
            else:
                self.lasers.add(new_laser)
            print("fire laser " , len(self.lasers.sprites()))

            '''laser weapon sfx'''
            # royalty free sfx from zapsplat.com
            weapon_laser_sound = pygame.mixer.Sound('game_audio/weapon_laser.wav')  # load sfx
            weapon_laser_sound.set_volume(0.3)
            weapon_laser_sound.play()  # play sfx

            # new_laser.update() #moving (should be updating)
        for laser in self.lasers.sprites():
            laser.draw_laser()
            laser.update()

class Enemy(Ship):
    # class variable to keep track of all enemy hitboxes
    enemies = list()

    def __init__(self, hp, x, y, speed):
        super(Enemy, self).__init__(hp, x, y, speed)
        self.enemyModel = pygame.image.load('game_images/Enemy.png')
        self.direction = random.randint(0, 3)
        self.change_direction = 0
        self.ship = self.enemyModel.get_rect()  # gets the rect of image
        Enemy.enemies.append(self)

    def __del__(self):
        Enemy.enemies.remove(self)

    # draw ship on screen
    def draw(self, window):
        Enemy.enemies.remove(self)
        self.ship.x, self.ship.y, self.ship.w, self.ship.h = self.x, self.y, 64, 64
        Enemy.enemies.append(self)
        window.blit(self.enemyModel, (self.x, self.y))

    # follows target within range, otherwise just move randomly
    def auto_movement(self, target):
        # check for bot collision here
        for x in Enemy.enemies:
            if self.ship != x.ship and self.collision(x.ship):
                self.direction = (x.direction + 2) % 4
                self.move_forward()
            else:
                dx, dy = target.x - self.x, target.y - self.y
                dist = math.hypot(dx, dy)
                # if in detection range
                if 350 > dist > 0:
                    dx, dy = dx / dist, dy / dist
                    self.x += dx * self.move_speed
                    self.y += dy * self.move_speed
                else:
                    self.change_direction = random.randint(0, 100)
                    if self.change_direction == 1:
                        self.direction = random.randint(0, 3)
                    self.move_forward()

    def move_forward(self, multiplier=1):
        if self.direction == 0:  # up
            self.y -= self.move_speed * multiplier
            if self.y < 5:
                self.direction = 2
        elif self.direction == 1:  # right
            self.x += self.move_speed * multiplier
            if self.x > 685:
                self.direction = 3
        elif self.direction == 2:  # down
            self.y += self.move_speed * multiplier
            if self.y > 685:
                self.direction = 0
        elif self.direction == 3:  # left
            self.x -= self.move_speed * multiplier
            if self.x < 5:
                self.direction = 1
