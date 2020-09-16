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

    def run_game(self):
        start = True

        player_ship = Player(100, 400, 400, 10)
        enemy_ship = Enemy(100, 200, 200, 10)  # instantiated here only for testing

        # Loops during runtime
        while start:
            self.clock.tick(60) # set framerate

            ''' USER INTERACTION '''
            # check screen size in case of resize
            w, h = pygame.display.get_surface().get_size()

            # mouse coordinates and keys pressed
            x, y = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            ''' MENU SECTION '''
            self.display.fill((0, 0, 0))
            self.add_text('Game Page', self.font, (255, 0, 0), self.display, 100, 0)

            # Buttons
            menu = pygame.Rect(0, 0, 80, 40)

            # if buttons are clicked actions
            if menu.collidepoint(x, y):
                if self.user_click:
                    self.user_click = False
                    self.menu()
            # Draw Button
            pygame.draw.rect(self.display, (192, 192, 192), menu)
            self.add_text('Menu', self.font, (255, 255, 255), self.display, 0, 5)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if keys[pygame.K_ESCAPE]:
                    start = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True

            ''' IN-GAME CODE '''
            player_ship.movement(keys, (w, h))
            enemy_ship.draw(self.display)
            player_ship.draw(self.display)
            pygame.display.update()


# can create other functions here to help run game


if __name__ == '__main__':
    # create game instance and run it
    svz = SpaceVentureZ()
    svz.menu()

''' 
run_game() in SpaceVentureZ overwrites the run_game in Display()
Note: place all game instances and functions for the game in run_game()
there is an example already placed

self.display is the window (changed the name from self.window) 
'''
