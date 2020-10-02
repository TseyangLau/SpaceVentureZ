import pygame
from pygame.locals import *


# creates the menu and user display
class Display:

    def __init__(self):
        """ initialize pygame and creates game title"""
        pygame.mixer.pre_init(44100, -16, 1, 512)  # for audio lag reduction
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('SpaceVentureZ')

        self.game_speed = 60;
        ''' Following are Display variables need for creation of display canvas'''
        self.background_color = (0, 0, 0)
        self.width = 750#600
        self.height = 750#1050
        self.font = pygame.font.SysFont('times new roman', 30)

        self.display = pygame.display.set_mode((self.width, self.height))

        '''variables that handles user mouse click on any display'''
        self.user_click = False

    '''Prints out text on the screen based on location x , y'''
    @staticmethod
    def add_text(text, font, color_, display, x, y):
        display.blit(font.render(text, True, color_), (x, y))
    '''Adds an image on the display screen'''
    @staticmethod
    def add_image(image, scale_w, scale_h, display, x, y):
        display.blit(pygame.transform.scale(image, (scale_w, scale_h)), (x, y))

    '''Display's game menu '''
    def menu(self):
        self.display = pygame.display.set_mode((600, 600))
        start = True

        '''Load's image'''
        game_Logo = pygame.image.load('game_images/SpaceVentureZ.png').convert()
        start_game = pygame.image.load('game_images/startButton.png').convert()
        options = pygame.image.load('game_images/optionButton.png').convert()
        screen = pygame.image.load('game_images/background.png').convert()

        '''load sfx'''
        menu_onclick = pygame.mixer.Sound('game_audio/menu_click.wav')

        while start:
            self.display.fill((0, 0, 0))

            '''Display Image logo AND Button images'''
            self.add_image(screen, 600, 600, self.display, 0, 0)
            self.add_image(game_Logo, 450, 350, self.display, 75, 0)
            self.add_image(start_game, 250, 85, self.display, 175, 200)
            self.add_image(options, 250, 85, self.display, 175, 285)

            '''gets user mouse click coordinates '''
            x, y = pygame.mouse.get_pos()

            '''Gets the rect from the images loaded and sets the position on display'''
            start_game_b = start_game.get_rect()
            start_game_b.x, start_game_b.y , start_game_b.w, start_game_b.h = (175, 200, 250, 85)
            options_b = options.get_rect()
            options_b.x, options_b.y, options_b.w, options_b.h = (175, 285, 250, 85)

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
                                menu_onclick.play()  # play menu click sfx
                                self.run_game()
                        if options_b.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                menu_onclick.play()  # play menu click sfx
                                self.options()
            pygame.display.update()
            self.clock.tick(60)

    def run_game(self):
        self.display = pygame.display.set_mode((self.width, self.height))
        start = True
        while start:
            self.display.fill((0, 0, 0))
            self.add_text('Game Page', self.font, (255, 0, 0), self.display, 100, 0)

            '''pygame event handling, exit and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.menu()

            '''Run and Update game display'''
            self.run()
            pygame.display.update()
            self.clock.tick(self.game_speed)

    ''' Display's Options Page'''
    def options(self):
        self.display = pygame.display.set_mode((600, 600))
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
                                '''sounds goes here'''
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
