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
        #print("This iss in the init of SHIP " , len(self.lasers.sprites()))

        '''load sfx'''
        # royalty free sfx from zapsplat.com
        self.weapon_laser_sound = pygame.mixer.Sound('game_audio/weapon_laser.wav')
        self.weapon_laser_sound.set_volume(0.2)

    def draw(self, window):
        self.ship = self.playerModel.get_rect() # gets the rect of image
        self.ship.x, self.ship.y, self.ship.w, self.ship.h = self.x, self.y, 64, 64
        window.blit(self.playerModel, (self.x, self.y))

    def movement(self, keys, boundary):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > self.move_speed - 20:
            self.x -= self.move_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < boundary[0] - 50:
            self.x += self.move_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > self.move_speed - 10:
            self.y -= self.move_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < boundary[1] - 50 - self.move_speed:
            self.y += self.move_speed

    def fire_laser(self, keys):
        pygame.key.set_repeat(0, 100)
        if keys[pygame.K_SPACE]:
            '''pygame.key.set_repeat(delay, interval) -> this is in milliseconds'''
            # set delay when the space key is held down
            #pygame.key.set_repeat(1, 100)
            # to print delay, for testing purposes
            #print(pygame.key.get_repeat())

            if len(self.lasers.sprites()) >= 60:
                # I don't know yet
                pass
            else:
                new_laser = Laser(self.x, self.y, self.display)
                self.lasers.add(new_laser)
            #print("fire laser " , len(self.lasers.sprites()))

            if self.is_sound_on:  # initial state
                self.weapon_laser_sound.play()  # play laser sfx

            # new_laser.update() #moving (should be updating)
        for laser in self.lasers.sprites():
            laser.draw_laser()
            laser.update()

    def draw_health_bar(self, display, x, y, max_health):
        # if max_health < 0:
        #   max_health = 0
        max_health = max(max_health, 0)
        BAR_LENGTH = 64
        BAR_HEIGHT = 10
        fill = (max_health / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        # the tuple after display is an rgb value, for the color of the bar and bar background
        pygame.draw.rect(display, (0, 255, 0), fill_rect)
        pygame.draw.rect(display, (255, 255, 255), outline_rect, 2)


class Enemy2(Ship):
    def __init__(self, hp, x, y, speed):
        Ship.__init__(self, hp, x, y, speed)
        self.enemyModel = pygame.image.load('game_images/boss.png')
        self.bossHit = pygame.image.load('game_images/boss_hit.png')
        self.ship = self.enemyModel.get_rect()  # gets the rect of image
        self.boss_is_hit = False

    def draw(self):
        self.ship.x, self.ship.y, self.ship.w, self.ship.h = self.x, self.y, 64, 64
        if self.boss_is_hit is False:
            self.display.blit(self.enemyModel, self.ship)
        else:
            self.display.blit(self.bossHit, self.ship)

    def auto_movement(self, target):
        dx, dy = target.x - self.x, target.y - self.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.x += dx * self.move_speed
        self.y += dy * self.move_speed

    def collision(self, obj2):
        return self.ship.colliderect(obj2)


class Enemy:
    # class variable to keep track of all enemy hit boxes
    enemies = list()
    direction = 0

    def __init__(self, hp, x, y, speed):
        self.enemyModel = pygame.image.load('game_images/Enemy.png')
        self.ship = self.enemyModel.get_rect()  # gets the rect of image
        self.health = hp
        self.x = x
        self.y = y
        self.move_speed = speed
        Enemy.enemies.append(self)

    def __del__(self):
        Enemy.enemies.remove(self)

    # draw ship on screen
    def draw(self, window):
        Enemy.enemies.remove(self)
        self.ship.x, self.ship.y, self.ship.w, self.ship.h = self.x, self.y, 64, 64
        Enemy.enemies.append(self)
        window.blit(self.enemyModel, (self.x, self.y))

    def auto_movement(self):
        # don't go offscreen
        for instance in Enemy.enemies:
            if instance.x < 0:
                Enemy.direction = 1
            if (instance.x + 64) > 750:
                Enemy.direction = 0
        # change direction randomly
        change_direction = random.randint(0, 500)
        if change_direction == 0:
            Enemy.direction = random.randint(0, 1)
        # progress movement
        if Enemy.direction == 0:
            self.x -= self.move_speed
        if Enemy.direction == 1:
            self.x += self.move_speed

    def collision(self, obj2):
        return self.ship.colliderect(obj2)


    # def auto_movement(self, target):
    #     # check for bot collision here
    #     for x in Enemy.enemies:
    #         if self.ship != x.ship and self.collision(x.ship):
    #             self.direction = (x.direction + 2) % 4
    #             #self.move_forward()
    #             x.movement()
    #         else:
    #             dx, dy = target.x - self.x, target.y - self.y
    #             dist = math.hypot(dx, dy)
    #             # if in detection range
    #             if 350 > dist > 0:
    #                 dx, dy = dx / dist, dy / dist
    #                 self.x += dx * self.move_speed
    #                 self.y += dy * self.move_speed
    #             else:
    #                 self.change_direction = random.randint(0, 100)
    #                 if self.change_direction == 1:
    #                     self.direction = random.randint(0, 3)
    #                 self.move_forward()
    #
    # def move_forward(self, multiplier=1):
    #     if self.direction == 0:  # up
    #         self.y -= self.move_speed * multiplier
    #         if self.y < 5:
    #             self.direction = 2
    #     elif self.direction == 1:  # right
    #         self.x += self.move_speed * multiplier
    #         if self.x > 685:
    #             self.direction = 3
    #     elif self.direction == 2:  # down
    #         self.y += self.move_speed * multiplier
    #         if self.y > 685:
    #             self.direction = 0
    #     elif self.direction == 3:  # left
    #         self.x -= self.move_speed * multiplier
    #         if self.x < 5:
    #             self.direction = 1
