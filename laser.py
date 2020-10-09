import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    """A class to manage lasers fired from ships."""

    def __init__(self,x, y, display): #ai_game
        """Create a laser object at the ship's current location."""
        super().__init__()
        '''the laser'''
        self.x = x
        self.y = y
        self.screen = display #ai_game.screen
        #self.settings = ai_game.settings
        self.color = (255, 0, 0) #self.settings.laser_color

        # Create a laser rect at (0,0) and then set current position.
        # self.x, self.y

        self.laser = pygame.Rect(self.x+31, self.y, 5, 5) #spawning
        #self.rect.midtop = ai_game.ship.rect.midtop

        # Store the laser's position as a decimal value.
        self.y = float(self.laser.y)

    def update(self):
        """Move the laser up the screen"""
        # Update the decimal position of the laser.
        self.y -= 4 #self.settings.laser_speed
        # Update the rect position
        self.laser.y = self.y

    def draw_laser(self):
        """Draw the laser to the screen"""
        pygame.draw.rect(self.screen, self.color, self.laser)
        #weapon_laser_sound = pygame.mixer.Sound('game_audio/weapon_laser.wav')
        #weapon_laser_sound.play()

