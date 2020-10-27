import pygame
from pygame.sprite import Sprite


class Virus(Sprite):
    """A class to represent a single virus"""

    def __init__(self, st_settings, screen):
        """Initialize the virus and set it's starting postion"""
        super().__init__()
        self.screen = screen
        self.st_settings = st_settings

        # load the virus image and set it's attribute
        self.image = pygame.image.load("images/virus_obj_small.bmp")
        self.rect = self.image.get_rect()

        # start the virus at the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the virus exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """draw the virus on the screen"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """update the position of virus"""
        self.x += (self.st_settings.virus_speed_factor *
                   self.st_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """If the virus rect is at the edge of the screen, it'll return true"""
        screen_rect = self.screen.get_rect()
        if self.rect.x >= screen_rect.right:
            return True
        elif self.rect.x <= 0:
            return True
