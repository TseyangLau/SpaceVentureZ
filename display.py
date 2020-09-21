import pygame
from pygame.locals import *

# creates user display
class Display:

    def __init__(self):
        """ initialize pygame and creates game title"""
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('SpaceVentureZ')

        ''' Following are Display variables need for creation of display canvas'''
        self.background_color = (0, 0, 0)
        self.width = 600
        self.height = 600
        self.font = pygame.font.SysFont('times new roman', 30)

        self.display = pygame.display.set_mode((self.width, self.height), RESIZABLE)

        '''variables that handles user mouse click on any display'''
        self.user_click = False

    '''Prints out text on the screen based on location x , y'''
    @staticmethod
    def add_text(text, font, color_, display, x, y):
        display.blit(font.render(text, True, color_), (x, y))

    def run_display(self):
        pass

    '''Display's game menu '''
    def menu(self):
        start = True
        while start:
            self.display.fill((0, 0, 0))

            '''gets user mouse click coordinates '''
            x, y = pygame.mouse.get_pos()

            '''Creates Buttons and draw's them on the display'''
            start_game_b = pygame.Rect(200, 150, 250, 50)
            options_b = pygame.Rect(200, 201, 250, 50)

            pygame.draw.rect(self.display, (255, 0, 0), start_game_b)
            self.add_text('Start Game', self.font, (255, 255, 255), self.display, 260, 160)
            pygame.draw.rect(self.display, (255, 255, 0), options_b)
            self.add_text('Options', self.font, (0, 0, 0), self.display, 263, 210)

            '''pygame event handling, exit and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
                        if start_game_b.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                self.run_game()
                        if options_b.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                self.options()
            pygame.display.update()
            self.clock.tick(60)

    def run_game(self):
        start = True
        while start:
            self.display.fill((0, 0, 0))
            self.add_text('Game Page', self.font, (255, 0, 0), self.display, 100, 0)

            '''gets user mouse click coordinates '''
            x, y = pygame.mouse.get_pos()

            '''Creates Buttons and draw's them on the display'''
            menu = pygame.Rect(0, 0, 80, 40)

            pygame.draw.rect(self.display, (192, 192, 192), menu)
            self.add_text('Menu', self.font, (255, 255, 255), self.display, 0, 5)

            '''pygame event handling, exit and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
                        if menu.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                self.menu()

            '''Run and Update game display'''
            self.run()
            pygame.display.update()
            self.clock.tick(60)

    ''' Dsiplay's Options Page'''
    def options(self):
        start = True
        while start:
            self.display.fill((0, 0, 0))
            self.add_text('Options Page', self.font, (255, 0, 0), self.display, 100, 0)

            # mouse coordinates
            x, y = pygame.mouse.get_pos()

            '''Creates Buttons and draw's them on the display'''
            menu = pygame.Rect(0, 0, 80, 40)

            pygame.draw.rect(self.display, (192, 192, 192), menu)
            self.add_text('Menu', self.font, (255, 255, 255), self.display, 0, 5)

            '''pygame event handling, exit and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
                        if menu.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                self.menu()
            pygame.display.update()
            self.clock.tick(60)

    '''added run here to be overwritten in the main.py'''
    def run(self):
        pass

'''
NOTE: options and menu are incomplete
was unable to condense code into smaller helper functions
'''

