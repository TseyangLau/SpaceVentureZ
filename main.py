# import sys
import pygame
from pygame.locals import *
from display import Display
from ships import Player
from ships import Enemy

class SpaceVentureZ(Display):
    def __init__(self):
        Display.__init__(self)  # keeps the inheritance of Display
        # set window icon
        # icon = pygame.image.load('...')
        # pygame.display.set_icon(icon)
        # game variables
        self.playerLifeCount = 100 
        
        # instantiated here only for testing
        self.player_ship = Player(self.playerLifeCount, 400, 400, 10)
        self.enemy_ship = Enemy(self.playerLifeCount, 200, 200, 10)
        
    ''' Runs the game overwrites the run in display.py which is currently empty '''    
    def run(self):
        # check screen size in case of resize
        w, h = pygame.display.get_surface().get_size()
        keys = pygame.key.get_pressed()

        '''In Game Code'''
        self.player_ship.movement(keys, (w, h))
        self.enemy_ship.draw(self.display)
        self.player_ship.draw(self.display)

# can create other functions here to help run game


if __name__ == '__main__':
    # create game instance and run it
    svz = SpaceVentureZ()
    svz.menu()

''' 
run() runs the game initially called in run_game in the Display class

self.display is the window (changed the name from self.window) 
'''
