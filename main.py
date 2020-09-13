import sys
import pygame
from shipbase import Ship

class SpaceVentureZ:
    def __init__(self):
        pygame.init()  # initiate pygame
        # window size
        background_color = (0, 0, 0)  # background change to black
        (width, height) = (600, 600)
        self.window = pygame.display.set_mode((width, height))
        self.window.fill(background_color)
        pygame.display.set_caption('SpaceVentureZ')
        # set window icon
        # icon = pygame.image.load('...')
        # pygame.display.set_icon(icon)
    def menu(self):
        pass #tbd will work on this
    def run_game(self):
        #testing only
        player_ship = Ship(100, 400, 400, 50)
        player_ship.draw(self.window)
        #end of testing
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

if __name__ == '__main__':
    # create game instance and run it
    svz = SpaceVentureZ()
    svz.run_game()
