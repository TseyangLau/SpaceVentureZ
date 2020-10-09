# import sys
import pygame
import random
from display import Display
from ships import Player
from ships import Enemy
from object import *
from laser import Laser


class SpaceVentureZ(Display):
    def __init__(self):
        Display.__init__(self)  # keeps the inheritance of Display

        # game variables life for entities
        self.playerLifeCount = 100
        self.enemyLifeCount = 1

        '''creation of entities'''
        self.player_ship = Player(self.playerLifeCount, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(random.randint(100, self.width-20), random.randint(200,600), 40, self.display)

        # initialization of enemies here (spawn too many and game will crash lol)
        # lets set a max ?? -isabel
        self.enemy_max = 50
        self.enemies = list()
        for x in range(10):
            self.enemies.append(Enemy(self.enemyLifeCount, random.randint(0, 686), random.randint(0, 686), 2))

        #@alfredo does this need to be here? -isabel
        # laser settings for player ship, placed here for now.
        self.laser_speed = 1.0
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = (60, 60, 60)
        self.lasers_allowed = 5

        #@alfredo does this need to be here? -isabel
        # storing lasers into a group
        self.lasers = pygame.sprite.Group()

    def run(self):
        # check screen size in case of resize
        w, h = pygame.display.get_surface().get_size()
        keys = pygame.key.get_pressed()

        '''In Game Code'''
        self.player_ship.movement(keys, (w, h))
        self.player_ship.fire_laser(keys)
        #self.player_ship.laser.draw_laser()
        #self.player_ship.laser.update()
        '''Draw objects on the display '''

        self.player_ship.draw(self.display)
        self.black_hole.draw()

        #self.player_ship.fire_laser(keys)
        self.lasers.update()
        # get rid of lasers that have gone off screen
        '''
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        print(len(self.lasers))
        '''
        #if len(self.enemies) == 0:
        #    self.paused() // its not working
        # maintaining enemies here
        #for x in range(len(self.enemies)):
        #    self.enemies[x].draw(self.display)
        #    self.enemies[x].collision(self.player_ship.ship)
        #    self.enemies[x].auto_movement(self.player_ship)

        for x in self.enemies:
            x.draw(self.display)
            x.collision(self.player_ship.ship)
            x.auto_movement(self.player_ship)
            print(x.health)

        if x.collision(self.player_ship.ship) == True:
            """if enemy ship collides with player ship, then player ship loses hp"""
            print("they touching")
            self.player_ship.health -= 100



            #handle enemies dying when health goes to 0 -isabel
            if x.health < 0:
                self.enemies.remove(x)
            '''black-hole handling for enemy ships; if ship touch black hole then
            a random num is generated if the random num is 1 the enemy dies 
            else it creates a new enemy spawn (@everyone this can be changed -isabel)'''
            if self.black_hole.entered_bh(x.ship):
                random_num = random.randint(0, 2)
                if random_num != 1:
                    self.enemies.remove(x)
                elif self.enemy_max >= len(self.enemies):
                    #self.black_hole.pulse()
                    self.enemies.append(Enemy(self.playerLifeCount, random.randint(0, 750), random.randint(0, 750), 2))

        ''' BLACK HOLE HANDLING for player ship need to implement a pause sequence '''
        if self.black_hole.entered_bh(self.player_ship.ship):
            self.black_hole.pulse()
            self.player_ship.x, self.player_ship.y = random.randint(0, self.width-50), random.randint(50, self.height)
            self.blipEffect(self.player_ship)

        '''Laser handling'''
        for p_laser in self.player_ship.lasers:
            '''if laser goes into black hole the laser disapears'''
            if self.black_hole.entered_bh(p_laser.laser):
                self.player_ship.lasers.remove(p_laser)
            '''if the laser goes into enemy ship?? life of ship decreases by 5? -isabel'''
            for x in self.enemies:
                if x.collision(p_laser.laser):
                    x.health -= 5
                    self.player_ship.lasers.remove(p_laser)


    def blipEffect(self, element):
        '''trying to get the game to pause and player to blip in and out indicating new location'''
        pass









# can create other functions here to help run game

if __name__ == '__main__':
    # create SpaceVentureZ game instance and run it
    svz = SpaceVentureZ()
    svz.run_game()

''' 
run() runs the game initially called in run_game in the Display class

self.display is the window (changed the name from self.window) 
'''
