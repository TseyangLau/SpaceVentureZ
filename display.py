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
        self.width = 750  # 600
        self.height = 800  # 1050
        self.font = pygame.font.SysFont('times new roman', 30)

        self.display = pygame.display.set_mode((self.width, self.height))

        '''variables that handles user mouse click on any display'''
        self.user_click = False

        '''variables that handle when game is paused'''
        self.pause = False

        '''user mouseover state variables'''
        self.start_mouseover_state = False
        self.options_mouseover_state = False

        '''user sound state variables'''
        self.is_sound_on = True

        '''variable that handles when the game is over'''
        self.game_over = False
        
        '''background that is going to be used for scrolling'''
        self.bgimage = pygame.image.load('game_images/sv_bg2.png')
        self.rectBGimg = self.bgimage.get_rect()
        self.bgY1 = 0
        self.bgX1 = 0
        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0
        self.moving_speed = 5

        ''' GAME '''

    '''Prints out text on the screen based on location x , y'''

    def add_text(self, text, font, color_, display, x, y):
        display.blit(font.render(text, True, color_), (x, y))
    '''Adds an image on the display screen'''
    @staticmethod
    def add_image(image, scale_w, scale_h, display, x, y):
        display.blit(pygame.transform.scale(image, (scale_w, scale_h)), (x, y))

    def hovered_image(self, image, image2, scale_w, scale_h, display, x, y):
        self.add_image(image2, scale_w+10, scale_h+10, display, x-4, y-4)
        self.add_image(image, scale_w, scale_h, display, x, y)

    '''Display's game menu '''
    def menu(self):
        start = True

        '''Load's image'''
        game_logo = pygame.image.load('game_images/SpaceVentureZ.png').convert()
        start_game = pygame.image.load('game_images/startButton.png').convert()
        #options = pygame.image.load('game_images/optionButton.png').convert()
        screen = pygame.image.load('game_images/background.png').convert()
        white_back = pygame.image.load('game_images/white_back.png').convert()
        star_point = pygame.image.load('game_images/star-point.png').convert()

        '''load sfx'''
        # royalty free sfx from zapsplat.com
        menu_onclick_sound = pygame.mixer.Sound('game_audio/menu_click.wav')
        menu_onclick_sound.set_volume(0.8)
        menu_mouseover_sound = pygame.mixer.Sound('game_audio/menu_mouseover.wav')
        menu_mouseover_sound.set_volume(0.7)

        '''menu background music'''
        # royalty free sfx from zapsplat.com
        #pygame.mixer.music.load('game_audio/bg_menu.wav')  # load menu bgm
        #pygame.mixer.music.set_volume(0.6)
        #pygame.mixer.music.play()  # play menu bgm

        while start:
            self.display.fill((0, 0, 0))

            '''Display Image logo AND Button images'''
            self.add_image(screen, self.width, self.height, self.display, 0, 0)
            self.add_image(game_logo, 450, 350, self.display, self.width/5, 0)
            self.add_image(start_game, 250, 85, self.display, self.width/3, 200)
            #self.add_image(options, 250, 88, self.display, self.width/3, 288)

            '''gets user mouse click coordinates '''
            x, y = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pos() #this is the same as the one above.. why repeat?

            '''Gets the rect from the images loaded and sets the position on display'''
            start_game_b = start_game.get_rect()
            start_game_b.x, start_game_b.y, start_game_b.w, start_game_b.h = (self.width/3, 200, 250, 85)
            # options_b = options.get_rect()
            # options_b.x, options_b.y, options_b.w, options_b.h = (self.width/3, 288, 250, 88)

            '''get mouseover state'''
            start_mouseover = start_game_b.x + start_game_b.w > mouse[0] > start_game_b.x and start_game_b.y + start_game_b.h > mouse[1] > start_game_b.y
            #options_mouseover = options_b.x + options_b.w > mouse[0] > options_b.x and options_b.y + options_b.h > mouse[1] > options_b.y

            '''pygame event handling, exit, mouseover, and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    start = False
                if event.type == MOUSEMOTION:
                    if start_mouseover and self.start_mouseover_state is False:
                        self.hovered_image(start_game, white_back, 250, 85, self.display, self.width/3, 200)
                        menu_mouseover_sound.play()  # play mouseover sfx
                        self.start_mouseover_state = True
                    if start_mouseover is False and self.start_mouseover_state is True:
                        self.start_mouseover_state = False  # reset mouseover
                    # if options_mouseover and self.options_mouseover_state is False:
                    #     self.hovered_image(options, white_back, 250, 88, self.display, self.width/3, 288)
                    #     menu_mouseover_sound.play()  # play mouseover sfx
                    #     self.options_mouseover_state = True
                    # if options_mouseover is False and self.options_mouseover_state is True:
                    #     self.options_mouseover_state = False  # reset mouseover
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
                        if start_game_b.collidepoint(x, y):
                            if self.user_click:
                                self.user_click = False
                                menu_onclick_sound.play()  # play menu click sfx
                                pygame.mixer.music.stop()  # stop menu bgm
                                self.restart()
                        # if options_b.collidepoint(x, y):
                        #     if self.user_click:
                        #         self.user_click = False
                        #         menu_onclick_sound.play()  # play menu click sfx
                        #         pygame.mixer.music.stop()  # stop menu bgm
                        #         self.options()
            pygame.display.update()
            self.clock.tick(60)

    def run_game(self):

        '''in-game background music'''
        # royalty free sfx from zapsplat.com
        #pygame.mixer.music.load('game_audio/bg_game.wav')  # load game bgm
        #pygame.mixer.music.set_volume(0.5)
        #pygame.mixer.music.play()  # play game bgm

        running = True
        while running:
            self.display.fill((0, 0, 0))

            '''pygame event handling, exit and user mouse click handling'''
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        #pygame.mixer.music.stop()  # stop game bgm
                        self.menu()
                    if event.key == pygame.K_p:
                        self.pause = True
                        #pygame.mixer.music.set_volume(0.1)  # reduce music volume
            '''Run and Update game display'''
            self.run()
            pygame.display.update()
            self.clock.tick(self.game_speed)

    ''' Display's Options Page'''
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
                                '''sounds goes here'''
                                self.menu()
            pygame.display.update()
            self.clock.tick(60)

    '''added run here to be overwritten in the main.py'''
    def run(self):
        pass

    '''display when pausing the game'''
    def paused(self):
        # text = pygame.font.SysFont('times new roman', 100)
        # self.add_text("PAUSED", text, (255, 0, 0), self.display, self.width / 4, self.height / 4)

        '''Add buttons with images and creates the buttons rect'''

        restart = pygame.image.load("game_images/restart.png")
        re_rect = restart.get_rect()
        re_rect.x, re_rect.y, re_rect.w, re_rect.h = self.width/4 - 50, self.height/3+50, 196, 80
        self.display.blit(restart, re_rect)

        resume = pygame.image.load("game_images/resume.png")
        res_rect = resume.get_rect()
        res_rect.x, res_rect.y, res_rect.w, res_rect.h = re_rect.x+res_rect.w+50, self.height/3 + 50, 196, 80
        self.display.blit(resume, res_rect)

        settings = pygame.image.load("game_images/settings.png")
        set_rect = settings.get_rect()
        set_rect.x, set_rect.y, set_rect.w, set_rect.h = 0, 0, 40, 40
        self.display.blit(settings, set_rect)

        sound_text = pygame.image.load("game_images/sound-text.png")
        sound_rect = sound_text.get_rect()
        sound_rect.x, sound_rect.y, sound_rect.w, sound_rect.h = self.width/4 - 10, re_rect.y + re_rect.h + 50, 123, 40

        sound_on = pygame.image.load("game_images/sound-on-text.png")
        sound_on_s = pygame.image.load("game_images/sound-on-s-text.png")
        son_rect = sound_on.get_rect()
        son_rect.x, son_rect.y, son_rect.w, son_rect.h = res_rect.x, sound_rect.y, 75, 40

        sound_off = pygame.image.load("game_images/sound-off-text.png")
        sound_off_s = pygame.image.load("game_images/sound-off-s-text.png")
        soff_rect = sound_off.get_rect()
        soff_rect.x, soff_rect.y, soff_rect.w, soff_rect.h = son_rect.x + son_rect.w + 45, son_rect.y, 75, 40

        '''display sound buttons'''
        self.display.blit(sound_text, sound_rect)
        if self.is_sound_on:  # initial state
            self.display.blit(sound_on_s, son_rect)
            self.display.blit(sound_off, soff_rect)
        else:
            self.display.blit(sound_on, son_rect)
            self.display.blit(sound_off_s, soff_rect)

        pygame.display.update()
        while self.pause:
            x, y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
                        if res_rect.collidepoint(x, y):
                            self.pause = False
                            self.user_click = False
                            # pygame.mixer.music.set_volume(0.5)  # increase music volume
                        if set_rect.collidepoint(x, y):
                            self.pause = False
                            self.user_click = False
                            self.options()
                        if re_rect.collidepoint(x,y):
                            self.pause = False
                            self.user_click = False
                            self.restart()
                        if son_rect.collidepoint(x, y):  # if user select on button
                            self.display.fill(0, soff_rect)
                            self.display.blit(sound_on_s, son_rect)
                            self.display.blit(sound_off, soff_rect)
                            pygame.display.update()
                            # pygame.mixer.music.unpause()
                            self.is_sound_on = True
                            self.user_click = False
                        if soff_rect.collidepoint(x, y):  # if user select off button
                            self.display.fill(0, son_rect)
                            self.display.blit(sound_on, son_rect)
                            self.display.blit(sound_off_s, soff_rect)
                            pygame.display.update()
                            # pygame.mixer.music.pause()
                            self.is_sound_on = False
                            self.user_click = False

    def end_screen(self, result):
        panel = Rect(0, 0, 750, 800)
        pygame.draw.rect(self.display, (0, 0, 0), panel)

        font = pygame.font.SysFont('times new roman', 100)
        text = font.render(result, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.width/2, self.height/2 - 50))
        self.display.blit(text, text_rect)

        restart = pygame.image.load("game_images/restart.png")
        re_rect = restart.get_rect()
        re_rect.x, re_rect.y, re_rect.w, re_rect.h = self.width / 2 - 100, self.height / 3 + 150, 196, 80
        self.display.blit(restart, re_rect)

        '''load sfx'''
        # royalty free sfx from zapsplat.com
        pygame.mixer.music.stop()  # stop game bgm
        if result == "Victory" and self.is_sound_on:
            pygame.mixer.music.load('game_audio/end_victory.wav')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()  # play victory sfx
        if result == "Defeat" and self.is_sound_on:
            pygame.mixer.music.load('game_audio/end_defeat.wav')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()  # play defeat sfx
        
        pygame.display.update()
        while self.game_over:
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.user_click = True
                        if re_rect.collidepoint(x, y):
                            self.game_over = False
                            self.user_click = False
                            pygame.mixer.music.stop() # stop endscreen sfx
                            self.restart()

    def restart(self):
        pass
    
    def update_background(self):
        """Handles all the movement of the background. Decrements y-coordinates every re-draw."""
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def render_background(self):
        """Draws the final background using both coordinates (top left corner and bottom right corner."""
        self.display.blit(self.bgimage, (self.bgX1, self.bgY1))
        self.display.blit(self.bgimage, (self.bgX2, self.bgY2))

'''
NOTE: options and menu are incomplete
was unable to condense code into smaller helper functions
'''
