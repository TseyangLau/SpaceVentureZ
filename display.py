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

        self.game_speed = 60
        ''' Following are Display variables need for creation of display canvas'''
        self.background_color = (0, 0, 0)
        self.width = 750 #600
        self.height = 800 #1050
        self.font = pygame.font.SysFont('times new roman', 30)

        self.display = pygame.display.set_mode((self.width, self.height))

        '''variables that handles user mouse click on any display'''
        self.user_click = False

        '''variables that handle when game is paused'''
        self.pause = False

        '''user mouseover state variables'''
        self.start_mouseover_state = False
        self.options_mouseover_state = False

        ''' GAME '''
        self.running = True
        self.player_alive = True

    '''Prints out text on the screen based on location x , y'''

    def add_text(self, text, font, color_, display, x, y):
        display.blit(font.render(text, True, color_), (x, y))
    '''Adds an image on the display screen'''
    @staticmethod
    def add_image(image, scale_w, scale_h, display, x, y):
        display.blit(pygame.transform.scale(image, (scale_w, scale_h)), (x, y))

    def hovered_image(self, image, image2, scale_w, scale_h, display, x, y):
        self.add_image(image2,scale_w+10, scale_h+10 , display, x-4, y-4)
        self.add_image(image, scale_w,scale_h,display, x, y)

    '''Display's game menu '''
    def menu(self):
        self.display = pygame.display.set_mode((600, 600))
        start = True

        '''Load's image'''
        game_Logo = pygame.image.load('game_images/SpaceVentureZ.png').convert()
        start_game = pygame.image.load('game_images/startButton.png').convert()
        options = pygame.image.load('game_images/optionButton.png').convert()
        screen = pygame.image.load('game_images/background.png').convert()
        white_back = pygame.image.load('game_images/white_back.png').convert()

        '''load sfx'''
        # royalty free sfx from zapsplat.com
        menu_onclick_sound = pygame.mixer.Sound('game_audio/menu_click.wav')
        menu_onclick_sound.set_volume(0.8)
        menu_mouseover_sound = pygame.mixer.Sound('game_audio/menu_mouseover.wav')
        menu_mouseover_sound.set_volume(0.7)

        '''menu background music'''
        # royalty free sfx from zapsplat.com
        pygame.mixer.music.load('game_audio/bgm.wav')  # load menu bgm
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play()  # play menu bgm

        while start:
            self.display.fill((0, 0, 0))

            '''Display Image logo AND Button images'''
            self.add_image(screen, 600, 600, self.display, 0, 0)
            self.add_image(game_Logo, 450, 350, self.display, 75, 0)
            self.add_image(start_game, 250, 85, self.display, 175, 200)
            self.add_image(options, 250, 88, self.display, 175, 288)

            '''gets user mouse click coordinates '''
            x, y = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pos()

            '''Gets the rect from the images loaded and sets the position on display'''
            start_game_b = start_game.get_rect()
            start_game_b.x, start_game_b.y , start_game_b.w, start_game_b.h = (175, 200, 250, 85)
            options_b = options.get_rect()
            options_b.x, options_b.y, options_b.w, options_b.h = (175, 288, 250, 88)

            '''get mouseover state'''
            start_mouseover = start_game_b.x + start_game_b.w > mouse[0] > start_game_b.x and start_game_b.y + start_game_b.h > mouse[1] > start_game_b.y
            options_mouseover = options_b.x + options_b.w > mouse[0] > options_b.x and options_b.y + options_b.h > mouse[1] > options_b.y

            '''pygame event handling, exit, mouseover, and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == MOUSEMOTION:
                    if start_mouseover and self.start_mouseover_state is False:
                        self.hovered_image(start_game, white_back, 250, 85, self.display, 175, 200)
                        menu_mouseover_sound.play()  # play mouseover sfx
                        self.start_mouseover_state = True
                    if start_mouseover is False and self.start_mouseover_state is True:
                        self.start_mouseover_state = False  # reset mouseover
                    if options_mouseover and self.options_mouseover_state is False:
                        self.hovered_image(options, white_back, 250, 88, self.display, 175, 288)
                        menu_mouseover_sound.play()  # play mouseover sfx
                        self.options_mouseover_state = True
                    if options_mouseover is False and self.options_mouseover_state is True:
                        self.options_mouseover_state = False  # reset mouseover
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
                        if start_game_b.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                menu_onclick_sound.play()  # play menu click sfx
                                pygame.mixer.music.stop()  # stop menu bgm
                                self.run_game()
                        if options_b.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                menu_onclick_sound.play()  # play menu click sfx
                                pygame.mixer.music.stop()  # stop menu bgm
                                self.options()
            pygame.display.update()
            self.clock.tick(60)

    def run_game(self):
        self.display = pygame.display.set_mode((self.width, self.height))

        '''in-game background music'''
        # royalty free sfx from zapsplat.com
        pygame.mixer.music.load('game_audio/bgm2.wav')  # load game bgm
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()  # play game bgm

        while self.running:
            self.display.fill((0, 0, 0))
            #self.add_text('Game Page', self.font, (255, 0, 0), self.display, 100, 0)

            '''pygame event handling, exit and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    self.running = False
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mixer.music.stop()  # stop game bgm
                        self.menu()
                    if event.key == pygame.K_p:
                        self.pause = True
                        pygame.mixer.music.pause()  # pause game bgm
                        self.paused()
            if self.player_alive == False:
                self.pause = True
                #self.paused()
                self.player_alive = True
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
            #self.clock.tick(60)

    '''added run here to be overwritten in the main.py'''
    def run(self):
        pass

    '''for pausing the game a work in progress'''
    def paused(self):
        text = pygame.font.SysFont('times new roman', 100)
        self.add_text("PAUSED", text, (255, 0, 0), self.display, 100, 100)
        pygame.display.update()

        while self.pause:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = False
                        pygame.mixer.music.unpause()  # unpause bgm
                        #self.run_game()
                        #self.menu()

            #pygame.display.update()
            self.clock.tick(15)



'''
NOTE: options and menu are incomplete
was unable to condense code into smaller helper functions
'''
