import pygame
from pygame.locals import *

''' creates the menu and user display'''
class Display:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('SpaceVentureZ')
        # screen size and color and font variables default
        self.background_color = (0, 0, 0)
        self.width = 600
        self.height = 600
        self.font = pygame.font.SysFont('times new roman', 30)

        self.display = pygame.display.set_mode((self.width, self.height), RESIZABLE)
        # set to false untill user clickes within a frame on display
        self.user_click = False

    def add_text(self, text, font, color, surface, x, y):
        surface.blit(font.render(text, True, color), (x, y))

    def menu(self):
        start = True
        while start:
            self.display.fill((0, 0, 0))

            # mouse coordinates
            x, y = pygame.mouse.get_pos()

            # Buttons
            start_game_b = pygame.Rect(200, 150, 250, 50)
            options_b = pygame.Rect(200, 201, 250, 50)

            # if buttons are clicked actions
            if start_game_b.collidepoint(x, y):
                if self.user_click:
                    self.user_click = False
                    self.run_game()
            if options_b.collidepoint(x, y):
                if self.user_click:
                    self.user_click = False
                    self.options()
            # Draw Button
            pygame.draw.rect(self.display, (255, 0, 0), start_game_b)
            self.add_text('Start Game', self.font, (255, 255, 255), self.display, 260, 160)
            pygame.draw.rect(self.display, (255, 255, 0), options_b)
            self.add_text('Options', self.font, (0, 0, 0), self.display, 263, 210)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        start = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
            pygame.display.update()
            self.clock.tick(60)

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

    def options(self):
        start = True
        while start:
            self.display.fill((0, 0, 0))
            self.add_text('Options Page', self.font, (255, 0, 0), self.display, 100, 0)

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


'''
Wasnt able to change the file name but class Display() will display 
the menu as well has handle user options of starting the game and changing to 
more options

NOTE: options is incomplete
'''
