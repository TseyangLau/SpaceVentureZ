# import sys
import pygame
import random
from display import Display
from ships import Player
from ships import Enemy
from obstacle import *
from laser import Laser


class SpaceVentureZ(Display):
    def __init__(self):
        Display.__init__(self)  # keeps the inheritance of Display

        # game variables life for entities
        self.playerHealthPoints = 100
        self.enemyHealthPoints = 1

        '''creation of entities'''
        self.player_ship = Player(self.playerHealthPoints, 400, 400, 10, self.display)  # added display
        self.black_hole = BlackHole(random.randint(100, self.width - 100), random.randint(100, 400), self.display)

        # initialization of enemies here (spawn too many and game will crash lol)
        # lets set a max ?? -isabel
        self.enemy_max = 50
        self.enemies = list()
        for x in range(2):
            self.enemies.append(Enemy(self.enemyHealthPoints, random.randint(0, 686), random.randint(0, 686), 2))

        #@alfredo does this need to be here? -isabel
        # laser settings for player ship, placed here for now.
        '''
        self.laser_speed = 1.0
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = (60, 60, 60)
        self.lasers_allowed = 5
        '''

        #@alfredo does this need to be here? -isabel
        # storing lasers into a group
        #self.lasers = pygame.sprite.Group()

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
        for x in self.enemies:
            x.draw(self.display)

        '''draws paused on display and handles unpause'''
        if self.pause:
            text = pygame.font.SysFont('times new roman', 100)
            self.add_text("PAUSED", text, (255, 0, 0), self.display, self.width/4, self.height/4)
            pygame.display.update()
            self.paused()

        #self.lasers.update()
        # get rid of lasers that have gone off screen
        '''
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        print(len(self.lasers))
        '''
        ''' Start of Enemy Ship Handling'''
        # while self.pause == False:
        for x in self.enemies:
            # x.draw(self.display) draws it before handling
            # x.collision(self.player_ship.ship)
            x.auto_movement(self.player_ship)
            # print(x.health)

            if x.collision(self.player_ship.ship):
                """if enemy ship collides with player ship, then player ship loses hp"""
                # print("they touching")
                self.player_ship.health -= 10
                if self.player_ship.health <= 0:
                    # print ("you died")
                    pass
                # del the player object

            # handle enemies dying when health goes to 0 -isabel
            if x.health <= 0:
                self.enemies.remove(x)

            '''black-hole handling for enemy ships currently removes enemy or teleports by random chance'''
            if self.black_hole.entered_bh(x.ship):
                random_num = random.randint(0, 2)
                if random_num != 1:
                    self.enemies.remove(x)
                # elif self.enemy_max >= len(self.enemies):
                    # self.black_hole.pulse()
                    # self.enemies.append(Enemy(self.playerHealthPoints, random.randint(0, 750), random.randint(0, 750), 2))
                else:
                    x.x, x.y = random.randint(64, self.width-64), random.randint(64, self.height-64)
        '''End of enemy ship handling'''

        ''' BLACK HOLE HANDLING for player ship need to implement a pause sequence '''
        if self.black_hole.entered_bh(self.player_ship.ship):
            self.black_hole.pulse()
            self.player_ship.x, self.player_ship.y = random.randint(0, self.width-64), random.randint(64, self.height)
            # self.blipEffect(self.player_ship)

        '''Laser handling with enemy ships'''
        for p_laser in self.player_ship.lasers:
            '''Delete laser when they go off screen'''
            if p_laser.y <= 0:
                print("OUT OF BOUNDS")
                self.player_ship.lasers.remove(p_laser)
                print(len(self.player_ship.lasers.sprites()))
            '''if laser goes into black hole the laser disappears'''
            if self.black_hole.entered_bh(p_laser.laser):
                self.player_ship.lasers.remove(p_laser)
            '''if the laser goes into enemy ship?? life of ship decreases by 5? -isabel'''
            for x in self.enemies:
                if x.collision(p_laser.laser):
                    x.health -= 1
                    self.player_ship.lasers.remove(p_laser.laser)

    def blipEffect(self, element):
        '''trying to get the game to pause and player to blip in and out indicating new location'''
        pass


if __name__ == '__main__':
    # create SpaceVentureZ game instance and run it
    svz = SpaceVentureZ()
    svz.run_game()

''' 
run() runs the game initially called in run_game in the Display class
self.display is the window (changed the name from self.window) 
'''
