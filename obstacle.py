from ships import *


class BlackHole:
    def __init__(self, x, y, radius, display):
        self.x = x
        self.y = y

        self.window = display
        self.radius = radius
        self.captured = []

        self.bh = None

    ''' draws the black-hole on the display'''

    def draw(self):
        self.bh = pygame.draw.circle(self.window, (0, 255, 0), (self.x, self.y), self.radius)
        #self.window.blit(pygame.transform.scale(self.black_hole_img, (self.w, self.h)), (self.x, self.y))
    ''' checks if the element was captured by black-hole'''

    def is_captured(self, element):
        return True if element in self.captured else False

    ''' moves the black-hole down the display'''

    def move(self):
        pass

    ''' black-hole pulses when an objects is captured'''

    def pulse(self):
        pygame.draw.circle(self.window, (255, 0, 0), (self.x, self.y), self.radius+20)
        #self.window.blit(pygame.transform.scale(self.black_hole_img2, (self.w+10, self.h+10)), (self.x, self.y))
        '''pulse sfx'''
        # royalty free sfx from zapsplat.com
        black_hole_sound = pygame.mixer.Sound('game_audio/black_hole.wav')  # load sfx
        black_hole_sound.play()  # play sfx

    '''returns true if the element entered within the surface area of the blackhole'''

    def entered_bh(self, element):
        return self.bh.colliderect(element)

