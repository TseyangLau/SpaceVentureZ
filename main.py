# import sys
import pygame
from pygame.locals import *
from shipbase import Ship
from display import Display

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
        while start:
            self.display.fill((0, 0, 0))
            self.add_text('Game Page', self.font, (255, 0, 0), self.display, 100, 0)

            # mouse coordinates
            x, y = pygame.mouse.get_pos()

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

            '''RUN GAME HERE'''

            player_ship = Ship(100, 400, 400, 50)
            player_ship.draw(self.display)

            # *************

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        start = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
            pygame.display.update()
            self.clock.tick(60)

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
